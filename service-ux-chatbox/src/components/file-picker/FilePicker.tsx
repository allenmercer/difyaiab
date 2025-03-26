import { useState } from 'react';
import axios from 'axios';
import { Button } from '../../../components/ui/button';
import { FileTrigger } from 'react-aria-components';
import { ListBox, ListBoxItem } from '../../components/ui/list-box';

const FilePicker = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const fileImport = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first');
      return;
    }

    const formData = new FormData();

    formData.append('file', selectedFile);
    formData.append('email', import.meta.env.VITE_EMAIL);
    formData.append('password', import.meta.env.VITE_PASSWORD);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    try {
      setUploadStatus('Importing...');
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND}/api/v1/import`,
        formData,
        config
      );
      console.log('response', response);
      setUploadStatus(`File Imported Successfully ${response.data.message}`);
    } catch (error) {
      setUploadStatus('An error occured during import');
    }
  };

  const clearFileSelected = () => {
    setSelectedFile(null);
  };
  return (
    <>
      <div className='flex-col'>
        <FileTrigger
          acceptedFileTypes={['.yml']}
          onSelect={(event) => {
            if (!event) return;
            let files = Array.from(event);
            setSelectedFile(files[0]);
          }}>
          <Button className='bg-blue-900 rounded-xl'>Select File</Button>
          <ListBox
            aria-label='Selected File'
            className='mt-2'
            style={{ display: selectedFile ? 'block' : 'none' }}>
            <ListBoxItem textValue='Files'>
              {selectedFile && selectedFile.name}
            </ListBoxItem>
          </ListBox>
        </FileTrigger>

        <div className='mt-6'>
          <Button
            className='bg-blue-900 rounded-xl'
            onPress={fileImport}
            isDisabled={!selectedFile}>
            Import DSL File
          </Button>
          <Button
            style={{ display: selectedFile ? 'inline-block' : 'none' }}
            className='bg-blue-900 ml-4 rounded-xl'
            onPress={clearFileSelected}
            isDisabled={!selectedFile}>
            Clear File
          </Button>
        </div>
        {uploadStatus && (
          <p className='mt-2 text-sm text-white'>{uploadStatus}</p>
        )}
      </div>
    </>
  );
};

export default FilePicker;
