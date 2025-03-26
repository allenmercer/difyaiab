import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatBot from './ChatBot';
import { vi } from 'vitest';

// Mock WebSocket
global.WebSocket = vi.fn(() => ({
  send: vi.fn(),
  close: vi.fn(),
  readyState: WebSocket.OPEN,
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
})) as unknown as typeof WebSocket;

describe('ChatBot Component', () => {
  test('renders ChatBot component correctly', () => {
    render(<ChatBot />);
    expect(
      screen.getByPlaceholderText(/Describe the workflow to create/i)
    ).toBeInTheDocument();
  });

  test('displays user message when sent', async () => {
    render(<ChatBot />);
    const input = screen.getByPlaceholderText(
      /Describe the workflow to create/i
    );
    const sendButton = screen.getByRole('button');

    fireEvent.change(input, { target: { value: 'Hello Bot!' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Hello Bot!')).toBeInTheDocument();
    });
  });

  test('disables input when WebSocket is not connected', () => {
    render(<ChatBot />);
    expect(
      screen.getByPlaceholderText(/Describe the workflow to create/i)
    ).toBeDisabled();
  });

  test('reconnects WebSocket on disconnect', async () => {
    const { rerender } = render(<ChatBot />);

    // Simulate WebSocket closing
    global.WebSocket.prototype.onclose?.({ code: 1000 } as CloseEvent);

    await waitFor(() => {
      rerender(<ChatBot />);
      expect(global.WebSocket).toHaveBeenCalled();
    });
  });
});
