import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import FilePicker from './FilePicker';
import { vi } from 'vitest';

vi.mock('axios');

describe('FilePicker Component', () => {
  it('renders select file button', () => {
    render(<FilePicker />);
    expect(screen.getByText('Select File')).toBeInTheDocument();
  });

  it('updates selected file name when a file is chosen', async () => {
    render(<FilePicker />);
    const file = new File(['dummy content'], 'test-file.txt', {
      type: 'text/plain',
    });
    const input = screen.getByText('Select File');

    await userEvent.upload(input, file);

    expect(screen.getByText('test-file.txt')).toBeInTheDocument();
  });

  it('disables the import button when no file is selected', () => {
    render(<FilePicker />);
    const importButton = screen.getByText('Import DSL File');
    expect(importButton).toBeDisabled();
  });

  it('enables the import button when a file is selected', async () => {
    render(<FilePicker />);

    const file = new File(['dummy content'], 'test-file.txt', {
      type: 'text/plain',
    });
    const input = screen.getByText('Select File');

    await userEvent.upload(input, file);

    const importButton = screen.getByText('Import DSL File');
    expect(importButton).not.toBeDisabled();
  });

  it('displays success message when file import is successful', async () => {
    (axios.post as jest.Mock).mockImplementation(() =>
      Promise.resolve({ data: { message: 'Import successful' } })
    );

    render(<FilePicker />);

    const file = new File(['dummy content'], 'test-file.txt', {
      type: 'text/plain',
    });
    const input = screen.getByText('Select File');

    await userEvent.upload(input, file);

    const importButton = screen.getByText('Import DSL File');
    fireEvent.click(importButton);

    await waitFor(() => {
      expect(
        screen.getByText('File Imported Successfully')
      ).toBeInTheDocument();
    });
  });

  it('displays error message when file import fails', async () => {
    (axios.post as jest.Mock).mockImplementation(() =>
      Promise.resolve(new Error('Import Failed'))
    );

    render(<FilePicker />);

    const file = new File(['dummy content'], 'test-file.txt', {
      type: 'text/plain',
    });
    const input = screen.getByText('Select File');

    await userEvent.upload(input, file);

    const importButton = screen.getByText('Import DSL File');
    fireEvent.click(importButton);

    await waitFor(() => {
      expect(
        screen.getByText('An error occured during import')
      ).toBeInTheDocument();
    });
  });
});
