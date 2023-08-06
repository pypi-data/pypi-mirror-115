import datetime
import os
from pathlib import Path

from pydicom import Dataset, FileDataset
from pydicom.dataset import FileMetaDataset

from aide_sdk.logger.logger import LogManager
from aide_sdk.model.operatorcontext import OperatorContext

logger_audit = LogManager._get_audit_logger()


def generate_random_uid():
    return '1.9.9.' + str(datetime.datetime.now().strftime('%H%M%S%f%d%m%Y'))


mount_path = os.getenv("INPUT_MOUNT", "")


class FileStorage:

    def __init__(self, context: OperatorContext):
        if not context:
            raise ValueError("Context can't be None")

        self.context = context
        self.mount_point = os.path.join(os.path.sep, mount_path)
        self.write_location = self._determine_write_location()

    def _determine_write_location(self):
        study_id = getattr(self.context.origin, 'study_uid', '')
        execution_uid = str(self.context._execution_context.execution_uid)

        write_location = os.path.join(self.context.origin.patient_id,
                                      study_id,
                                      self.context._correlation_id,
                                      self.context._execution_context.model_name,
                                      self.context._execution_context.model_version,
                                      execution_uid)
        return write_location

    def save_file(self, file_bytes: bytes, file_name) -> str:
        """
        Save binary data to disk.
        :file_bytes: The binary data of the file
        :file_name: The file name & extension.

        Returns the new file path.
        """
        try:
            folder = os.path.join(self.mount_point, self.write_location)
            os.makedirs(folder, exist_ok=True)
            file_location = os.path.join(self.write_location, file_name)
            absolute_path = os.path.join(self.mount_point, file_location)
            with open(absolute_path, 'wb') as f:
                f.write(file_bytes)

            logger_audit.info("Model has saved resource to file storage",
                              extra={"props": {
                                  "data": {
                                      "file": file_name
                                  }
                              }})
            return absolute_path
        except Exception:
            logger_audit.exception("Could not save file to storage",
                                   extra={"props": {
                                       "data": {
                                           "file": file_name
                                       }
                                   }})
            raise

    def load_file(self, file_path: str) -> bytes:
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
        except (FileNotFoundError, OSError, IOError):
            logger_audit.exception("Could not load file from file storage",
                                   extra={"props": {
                                       "data": {
                                           "file": file_path
                                       }
                                   }})
            raise
        else:
            logger_audit.info("Loaded file from file storage",
                              extra={"props": {
                                  "data": {
                                      "file": file_path
                                  }
                              }})
            return data

    def _get_absolute_path(self, path: str):
        return os.path.join(self.mount_point, path)

    def save_dicom(self, folder_name: str, dataset: Dataset) -> str:
        """
        Save a single DICOM image.
        DICOM images can only be saved as part of a study. Therefore
        a folder structure will be created, like this:
        WRITE_LOCATION/:folder_name:/{StudyInstanceUID}/{SeriesInstanceUID}/{SOPInstanceUID}.dcm

        :returns: the path to the study folder.
        """
        try:
            # Use existing study ID, if one exists
            study_id = getattr(self.context.origin, 'study_uid',
                               str(dataset.StudyInstanceUID))
            series_id = str(dataset.SeriesInstanceUID)
            sop_id = str(dataset.SOPInstanceUID)

            # Dicom folder within AIDE storage
            dicom_folder_path = os.path.join(self.write_location, folder_name)

            # Now generate DICOM folder hierarchy
            study_path = os.path.join(dicom_folder_path, study_id)
            absolute_study_path = self._get_absolute_path(study_path)

            series_path = os.path.join(study_path, series_id)
            absolute_series_path = self._get_absolute_path(series_path)

            # Actual DCM file path
            image_path = os.path.join(series_path, f"{sop_id}.dcm")
            absolute_image_path = self._get_absolute_path(image_path)

            # Create folder & write DICOM
            os.makedirs(absolute_series_path, exist_ok=True)
            dataset.save_as(absolute_image_path, write_like_original=False)
            logger_audit.info("Model has stored DICOM image dataset to storage",
                              extra={"props": {
                                  "data": {
                                      "file": absolute_image_path
                                  }
                              }})

            return absolute_study_path
        except ValueError:
            logger_audit.exception(
                "Failed to save DICOM Image. Value Error"
            )
            raise

        except AttributeError:
            logger_audit.exception(
                "Failed to save DICOM Image. Attribute Error"
            )
            raise

    def save_encapsulated_pdf(self,
                              folder_name: str,
                              dataset: Dataset,
                              pdf_file_path) -> str:
        try:
            file_name = Path(pdf_file_path).stem
            file_meta = FileMetaDataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'
            file_meta.MediaStorageSOPInstanceUID = (
                '2.16.840.1.114430.'
                '287196081618142314176776725491661159509.60.1'
            )
            file_meta.ImplementationClassUID = '1.3.46.670589.50.1.8.0'
            file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'

            ds = FileDataset(f"{file_name}.dcm", dataset,
                             file_meta=file_meta, preamble=b"\0" * 128)

            ds.PatientID = dataset.PatientID
            ds.StudyInstanceUID = dataset.StudyInstanceUID
            ds.SeriesInstanceUID = dataset.SeriesInstanceUID
            ds.SOPInstanceUID = generate_random_uid()  # generate random SOP id

            ds.is_little_endian = True
            ds.is_implicit_VR = False

            dt = datetime.datetime.now()
            ds.ContentDate = dt.strftime('%Y%m%d')
            time_str = dt.strftime('%H%M%S.%f')
            ds.ContentTime = time_str

            ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'

            with open(pdf_file_path, 'rb') as file:
                ds.EncapsulatedDocument = file.read()

            ds.MIMETypeOfEncapsulatedDocument = 'application/pdf'

            ds.Modality = 'DOC'
            ds.ConversionType = 'WSD'
            ds.SpecificCharacterSet = 'ISO_IR 100'

            logger_audit.info("PDF has been encapsulated")
            return self.save_dicom(folder_name, ds)

        except FileNotFoundError:
            logger_audit.exception("Failed to open PDF File")
            raise
