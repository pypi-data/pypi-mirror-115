"""
This file will contain general functions to help complete processes.
"""
# Initial Config
from datetime import date, datetime
from io import StringIO
import google.auth
from google.cloud import storage
from google.cloud import bigquery
from google.cloud import bigquery_storage
import pandas as pd
import os
from google.oauth2 import service_account
import sqlalchemy
import smtplib
import ssl


class Logging:
    """
    Logs all messages and outputs from the pipeline process. Note that this class needs a GCP
    bucket name to log all messages to.

    """

    def __init__(self, bucket_name: str):
        """
        The initialisation of the Logging class.

        Parameters
        ----------
        bucket_name: str, the bucket name of the GCP bucket.

        """
        self.bucket_name = bucket_name

    @staticmethod
    def create_filename() -> str:
        """
        Creates a filename with the latest date.

        Returns
        -------
        A filename with the latest date.

        """
        today = date.today()
        d1 = today.strftime("%d_%m_%Y")

        return "mapis_pipeline_log_" + d1 + ".txt"

    @staticmethod
    def create_dateformat(_format: str) -> str:
        """
        Creates the dateformat as a string based on the _format param.

        Parameters
        ----------
        _format: str, the format of what the datetime object should be.

        Returns
        -------
        A string with the datetime object formatted.

        """
        now = datetime.now()

        return now.strftime(_format)

    @staticmethod
    def instantiate_log(initial_entry: str):
        """
        The log is instantiated using the StringIO method to set as the file object.

        Parameters
        ----------
        initial_entry: str, the initial log entry.

        Returns
        -------
        The log instantiated.

        """
        return StringIO(initial_entry)

    @staticmethod
    def read_file(file):
        """
        The file object created from the func instantiate_log being read in.

        Parameters
        ----------
        file: the StringIO object created from the func instantiate_log.

        Returns
        -------
        A StringIO file object being read.

        """
        return file.read()

    def write_to_file(self, file, log: str):
        """
        Writes to the file object created beforehand.
        Parameters
        ----------
        file: the StringIO object created from the func instantiate_log.
        log: str, the message to log.

        Returns
        -------
        The StringIO file object updated with the log message.

        """
        return file.write(
            "\n"
            + Logging(bucket_name=self.bucket_name).create_dateformat(
                "%d-%b-%y %H:%M:%S"
            )
            + " - "
            + log
        )

    @staticmethod
    def seek_file(file):
        """
        Changes the stream position of the StringIO file object to the given
        byte offset.

        Parameters
        ----------
        file: the StringIO object created from the func instantiate_log.

        Returns
        -------
        The StringIO file object stream changed.

        """
        return file.seek(0)

    def upload_log(self, project: str, file):
        """
        The log file being uploaded to the 'logs' folder in the specified
        GCP bucket.

        Parameters
        ----------
        project: str, the GCP project name.
        file: the StringIO object created from the func instantiate_log.

        Returns
        -------
        The StringIO file object upload to a GCP bucket.

        """
        client = storage.Client(project=project)
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(
            "logs/" + Logging(bucket_name=self.bucket_name).create_filename()
        )

        return blob.upload_from_string(file.getvalue(), content_type="text")


class GCP:
    """
    Class contains function to handle processes in Google Cloud Platform.

    """
    def __init__(self):
        pass

    @staticmethod
    def upload_to_gcp_bucket(
            project: str, bucket_name: str, file_name: str, file_path: str
    ):
        """
        Uploads a file onto a GCP bucket specified.

        Parameters
        ----------
        project: str. The project name specified, eg, "omd-emea-daimler".
        bucket_name: str. The name of the bucket specified, eg "amq-daimler-competitive-mapis".
        file_name: str. The name of the file to upload. eg "data.txt".
        file_path: str. The name of the whole file to upload, eg "/home/jupyter/daimler_mapis_automation/data/txt/data.txt".

        Returns
        -------
        Uploads file to a specified GCP bucket.

        """
        client = storage.Client(project=project)
        bucket = client.get_bucket(bucket_name)

        blob = bucket.blob("raw/" + file_name)
        blob.upload_from_filename(file_path)
        print("----------------------")
        print(f"File {file_name} uploaded to {bucket.name}")

    @staticmethod
    def upload_df_to_bq(df: pd.DataFrame, table_id: str, data_dict: dict):
        """
        Uploads a specified dataframe to a specified BigQuery table. Note that you have to provide
        a data_dict which explicitly tells BigQuery what the column names are what their data types
        should be.

        Parameters
        ----------
        df: pd.DataFrame. A pandas dataframe input.
        table_id: str. The name of the table to be uploaded to. Note that if the table does not exist, a new one
        will be created according the table_id input. Eg, "omd-emea-daimler.Daimler_Competitive.registration_upload"
        data_dict: dict. The dict containing the columns in the dataframe with their respective data types.

        Returns
        -------
        Pandas dataframe uploaded to a BigQuery table.

        """
        print("----------------------")
        print("Initialising client")
        client = bigquery.Client()

        # Creating Schema
        print("----------------------")
        print("Creating schema")
        schema = []
        for key, value in data_dict.items():
            if value == "str":
                bq_val = "STRING"
            elif value == "int":
                bq_val = "INTEGER"
            elif value == "datetime64[ns]":
                bq_val = "DATE"
            elif value == "float64":
                bq_val = "FLOAT"
            else:
                bq_val = "STRING"

            schema_val = bigquery.SchemaField(f"{key}", f"{bq_val}")
            schema.append(schema_val)

        print("----------------------")
        print("Creating job config")
        job_config = bigquery.LoadJobConfig(schema=schema)

        print("----------------------")
        print("Initialising job")
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

        job.result()

        print("----------------------")
        print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns to {table_id}")

    @staticmethod
    def handle_credentials(credentials_path: str = None):
        """
        Handles the credentials initialisation depending on the environment being run in:
        either locally, or in a ComputeEngine account within the relevant GCP project.

        Parameters
        ----------
        credentials_path: str, the path to the credentials, note that this will need to be passed
        off if running locally.

        Returns
        -------
        A credentials param.

        """
        error_msg = ""

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        except Exception as e:
            error_msg = repr(e)

        if error_msg == "KeyError('GOOGLE_APPLICATION_CREDENTIALS')":
            credentials, your_project_id = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        else:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

            credentials = service_account.Credentials.from_service_account_file(
                filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

        return credentials

    @staticmethod
    def bq_table_to_dataframe(table_name: str, project_id: str, credentials_path: str = None) -> pd.DataFrame:
        """
        Downloads a whole table from a specified BigQuery table as a pandas dataframe.
        Note that the project_id & in_VM param handle the authentication of the relevant credentials;
        uses the handle_credentials func.

        Parameters
        ----------
        table_name: str. The name of the table from which the data is queried,
        eg "omd-emea-daimler.Daimler_Competitive.registration_upload_test".
        project_id: str. The name of the project id, eg: omd-emea-daimler.
        credentials_path: str. The path where the credentials for a GCP connection are stored, required if func is being
        run locally.

        Returns
        -------
        pd.DataFrame. A pandas dataframe.

        """
        print("----------------------")
        print("Initialising credentials")
        credentials = GCP.handle_credentials(credentials_path=credentials_path)

        print("----------------------")
        print("Establishing connection with BigQuery")
        bqclient = bigquery.Client(
            credentials=credentials,
            project=project_id,
        )

        bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

        query_string = f"""SELECT * FROM {table_name}"""

        print("----------------------")
        print("Executing query and returning dataframe")
        return (
            bqclient.query(query_string)
                .result()
                .to_dataframe(bqstorage_client=bqstorageclient)
        )

    @staticmethod
    def execute_sql_statement(sql_statement: str, table_id: str, query_parameters: list):
        """
        Executes a general SQL statement in BigQuery.

        Parameters
        ----------
        sql_statement: str, the SQL statement to be executed.
        table_id: str, the table name to be processed.
        query_parameters: list, the list of parameters to be considered when processing the job.

        Returns
        -------
        The sql statement executed in BigQuery.

        """
        client = bigquery.Client()

        destination_table = client.get_table(table_id)
        number_of_rows_before = destination_table.num_rows

        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)

        query_job = client.query(sql_statement, job_config=job_config)

        print("BigQuery (delete_from_bigquery): Starting job {}".format(query_job.job_id))
        query_job.result()  # awaits result of job

        ## get total number of rows after
        destination_table = client.get_table(table_id)
        number_of_rows_after = destination_table.num_rows

        print(
            "BigQuery (delete_from_bigquery): Job finished. Deleted {} rows.".format(
                -1 * (number_of_rows_after - number_of_rows_before)
            )
        )


class CloudSQL:
    """
    Class contains functions to handle processes in Cloud SQL.

    """
    def __init__(self):
        pass

    @staticmethod
    def create_cloud_sql_pool(
            db_user: str,
            db_pass: str,
            db_hostname: str,
            db_port: str,
            db_name: str,
            sslcert_path: str,
            sslkey_path: str,
            sslrootcert_path: str,
    ):
        """
        Establishes connection to a CloudSQL instance using the relevant credentials. Note that the relevant
        SSL certifications will need to be set up and downloaded as a prerequisite.

        Parameters
        ----------
        db_user: str. The username, eg "postgres".
        db_pass: str. The required password.
        db_hostname: str. The hostname of the CloudSQL instance, eg "35.246.119.155".
        db_port: str. The port of the CloudSQL instane, eg "5432".
        db_name: str. The name of the database to connect to, eg "postgres".
        sslcert_path: str. The path of the certification.
        sslkey_path: str. The path of the key certificate.
        sslrootcert_path: str. The path of the root certificate.

        Returns
        -------
        If all params are correct then a successful connection with a cloud SQL instance.

        """
        db_config = {
            "pool_size": 5,
            "max_overflow": 2,
            "pool_timeout": 30,
            "pool_recycle": 1800,
        }

        try:
            print("----------------------")
            print("Connection successful")
            pool = sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL(
                    drivername="postgresql+psycopg2",
                    username=db_user,
                    password=db_pass,
                    host=db_hostname,
                    port=db_port,
                    database=db_name,
                    query={
                        "sslcert": sslcert_path,
                        "sslkey": sslkey_path,
                        "sslrootcert": sslrootcert_path,
                    },
                ),
                **db_config,
            )

            return pool
        except:
            print("----------------------")
            print("Could not connect to database")

    @staticmethod
    def connect_to_cloud_sql(pool: sqlalchemy.engine):
        """
        Establishes a connection to the CloudSQL instance specified in the create_CloudSQL_pool function.
        """
        print("----------------------")
        print("Creating connection with CloudSQL instance")
        return pool.connect()

    @staticmethod
    def get_data_from_cloud_sql(
            pool: sqlalchemy.engine, query: str
    ) -> pd.DataFrame:
        """
        Gets data in the form of a pandas dataframe from the connection established using the
        connect_to_CloudSQL function.

        Parameters
        ----------
        pool: sqlalchemy.engine. The connection with the CloudSQL instance.
        query: str. The query string to execute, eg "SELECT * FROM 'table_name'".

        Returns
        -------
        pd.DataFrame. A pandas dataframe.

        """
        print("----------------------")
        print("Executing query")
        df = pd.read_sql_query(query, con=pool)

        print("----------------------")
        print("Returning dataframe")
        return df

    @staticmethod
    def upload_df_to_cloud_sql(
            df: pd.DataFrame, cloud_sql_table_name: str, pool: sqlalchemy.engine
    ):
        """
        Uploads a dataframe to a specified table in a CloudSQL instance based on a prior established connection.

        Parameters
        ----------
        df: pd.DataFrame. A pandas dataframe input.
        cloud_sql_table_name: str. The name of the table to upload the data, eg "mapis-registration".
        pool: sqlalchemy.engine. The connection to a specific CloudSQL instance,
        created using the create_CloudSQL_pool function.

        Returns
        -------
        Pandas dataframe uploaded onto a CloudSQL instance table.

        """

        print("----------------------")
        print(f"Uploading dataframe to CloudSQL instance - {cloud_sql_table_name}")
        return df.to_sql(cloud_sql_table_name, pool, if_exists="append", index=False)


class General:
    """
    Class contains generic functions that may be useful.

    """
    def __init__(self):
        pass

    @staticmethod
    def save_as_parquet(df: pd.DataFrame, save_path: str):
        """
        Saves off a dataframe as a parquet file to a specified location.

        Parameters
        ----------
        df: pd.DataFrame. A pandas dataframe input.
        save_path: str. The save_path where the dataframe should be saved off.

        Returns
        -------
        Pandas dataframe saved off as a parquet file.

        """
        print("----------------------")
        print("Saving off dataframe as a parquet file")
        df.to_parquet(save_path)

    @staticmethod
    def send_email_func(
        receiver_email: str, message: str, username: str, password: str
    ):
        """
        Sends an email address for the specified email address and category.

        Parameters
        ----------
        receiver_email: str. The email address of the sender, eg john_smith@gmail.com.
        message: str. The message to send to the specified user.
        username: str. The username of the sender.
        password: str. The password of the sender account.

        Returns
        -------
        An email sent to the user specified.

        """
        print(f"Sending email to {receiver_email}")
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = username
        password = password

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)