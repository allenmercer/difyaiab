import { useEffect, useRef, useState } from 'react';
import { Button } from '../../../components/ui/button';
import './chat-bot.css';
import axios from 'axios';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const CHAT_STORAGE_KEY = 'chat_messages';

const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [botResponse, setBotResponse] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const chatContainerRef = useRef<HTMLDivElement | null>(null);
  const reconnectIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const MAX_RETRIES = 5;
  let retryCount = 0;

  useEffect(() => {
    const savedMessages = localStorage.getItem(CHAT_STORAGE_KEY);

    if (savedMessages) {
      setMessages(JSON.parse(savedMessages));
    }
  }, []);

  const connectWebSocket = () => {
    if (socketRef.current && socketRef.current.readyState !== WebSocket.CLOSED)
      return;

    socketRef.current = new WebSocket(
      `${import.meta.env.VITE_WEBSOCKET_BACKEND}/api/v1/chat`
    );

    socketRef.current.onopen = () => {
      console.log('WebSocket connected');

      retryCount = 0;
    };

    socketRef.current.onmessage = (event) => {
      setIsBotTyping(false);
      const botMessage: Message = { sender: 'bot', text: event.data };
      updateMessages(botMessage);
      if (botMessage) setBotResponse(true);
    };

    socketRef.current.onerror = (error) => {
      console.log('WebSocket error', error);
    };

    socketRef.current.onclose = () => {
      console.log('WebSocket disonnected, retrying in 3 seconds...');

      if (retryCount < MAX_RETRIES) {
        retryCount++;
        if (reconnectIntervalRef.current !== null) {
          clearTimeout(reconnectIntervalRef.current);
        }
        reconnectIntervalRef.current = setTimeout(connectWebSocket, 3000);
      } else {
        console.error('Max reconnection attempts reached. Stopping retries');
      }
    };
  };

  useEffect(() => {
    connectWebSocket();

    return () => {
      socketRef.current?.close();
      if (reconnectIntervalRef.current)
        clearTimeout(reconnectIntervalRef.current);
    };
  }, []);

  const updateMessages = (newMessage: Message) => {
    setMessages((prev) => {
      const updateMessages = [...prev, newMessage];
      localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(updateMessages));
      return updateMessages;
    });

    scrollToBottom();
  };

  const sendMessage = () => {
    if (
      !input.trim() ||
      !socketRef.current ||
      socketRef.current.readyState !== WebSocket.OPEN
    ) {
      console.error('WebSocket is not open or message is empty');
      return;
    }

    const userMessage: Message = { sender: 'user', text: input };
    updateMessages(userMessage);

    setIsBotTyping(true);
    socketRef.current.send(input);
    setInput('');
  };

  const scrollToBottom = () => {
    setTimeout(() => {
      if (chatContainerRef.current) {
        chatContainerRef.current.scrollTop =
          chatContainerRef.current.scrollHeight;
      }
    }, 100);
  };

  const fileImport = async () => {
    const botMessages = messages.filter((message) => message.sender === 'bot');
    const botResponse = botMessages.map((message) => message.text);

    const payload = {
      file: botResponse[botResponse.length - 1],
      email: import.meta.env.VITE_EMAIL,
      password: import.meta.env.VITE_PASSWORD,
    };

    const config = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    try {
      setUploadStatus('Importing...');
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND}/api/v1/import_from_chat`,
        payload,
        config
      );
      if (response) setBotResponse(false);
      console.log('response.data', response.data);
      setUploadStatus('File Imported Successfully');
    } catch (error) {
      console.error('Error importing bot response');
    }
  };

  const clearMessages = () => {
    setMessages([]);
    localStorage.removeItem(CHAT_STORAGE_KEY);
  };

  return (
    <>
      <div className='flex justify-center bg-black'>
        <div
          className='flex flex-col rounded-lg my-5'
          style={{ width: '60%', height: '85vh' }}>
          <div className='flex-1 p-4 overflow-y-auto' ref={chatContainerRef}>
            {messages.length === 0 ?
              <div className='text-center text-gray-500'>
                <div className='text-4xl'>▲ + 💭</div>
                <p className='mt-2'>
                  This is an Agent Workflow generator built with <br />
                  React+MobX and the [AI]levate Agent Platform. <br />
                  It generates Dify.ai workflows and [AI]levate agentic <br />
                  capabilities to achieve business-specific tasks.
                </p>

                <p className='mt-2'>
                  You can learn more about [AI]levate platform <br />
                  capabilities by reading the{' '}
                  <span
                    className='font-bold underline'
                    style={{ cursor: 'pointer' }}>
                    docs
                  </span>
                </p>
              </div>
            : <>
                {messages.map((message, index) => (
                  <div key={index} className='mb-2 rounded-lg px-3 py-2'>
                    <div
                      className={`flex items-end mb-2 ${
                        message.sender === 'user' ?
                          'justify-end'
                        : 'justify-start'
                      }`}>
                      <div
                        className={`max-w-md p-3 rounded-lg whitespace-pre-wrap ${
                          message.sender === 'user' ?
                            'bg-white text-black ml-auto'
                          : 'bg-[#27272A] text-white mr-auto border-2 border-white p-4 rounded-xl'
                        }`}>
                        {message.text || (message.sender === 'bot' && '...')}
                      </div>
                    </div>
                  </div>
                ))}
                {isBotTyping && (
                  <div className='mb-2 rounded-lg px-3 py-2'>
                    <div className='flex items-end mb-2 justify-start'>
                      <div className='max-w-md rounded-lg whitespace-pre-wrap bg-gray-700 text-white mr-auto'>
                        ...
                      </div>
                    </div>
                  </div>
                )}
              </>
            }
          </div>

          <div className='flex items-center border-t p-4 input-container'>
            <div className='flex flex-1 items-baseline'>
              <input
                className='flex-1 border-2 p-2 rounded-lg bg-black text-white'
                style={{ height: '5.2em' }}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder='Describe the workflow to create...'
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    sendMessage();
                  }
                }}
              />
              <button
                className=' bg-gray-600 text-white rounded-r-lg hover:bg-blue-900 text-lg rounded-xl'
                style={{
                  borderRadius: '50%',
                  height: '2.2em',
                  width: '1em',
                  paddingRight: '1.3em',
                  marginLeft: '.5em',
                }}
                onClick={sendMessage}>
                ↑
              </button>
            </div>
          </div>
          <div
            className='flex border-t p-4 input-container'
            style={{ justifyContent: 'space-between' }}>
            <Button
              isDisabled={messages.length === 0 || !botResponse}
              className='w-40 ml-4 bg-blue-900 rounded-xl'
              onPress={fileImport}>
              Import File From Chat
            </Button>
            <p className='mt-2 text-sm text-white'>{uploadStatus}</p>
            <Button
              className='w-24 ml-4 bg-red-600 rounded-xl'
              onPress={clearMessages}
              isDisabled={messages.length === 0}>
              Clear Chat
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatBot;
