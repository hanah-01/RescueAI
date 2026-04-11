import { useState, useRef, ChangeEvent, KeyboardEvent } from 'react';
import './App.css';

interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  imageUrl?: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputVal, setInputVal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = async () => {
    if (!inputVal.trim() && !selectedImage) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: inputVal,
      imageUrl: selectedImage ? URL.createObjectURL(selectedImage) : undefined,
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputVal('');
    setSelectedImage(null);
    setIsLoading(true);

    try {
      if (newMessage.imageUrl) {
        const formData = new FormData();
        if (selectedImage) formData.append('file', selectedImage);
        formData.append('message', newMessage.text || '');

        const res = await fetch('http://localhost:8000/api/upload', {
          method: 'POST',
          body: formData,
        });
        const data = await res.json();
        
        const botMessage: Message = {
          id: Date.now().toString(),
          sender: 'bot',
          text: data.reply || 'Image processed successfully.',
        };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        const res = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: newMessage.text }),
        });
        const data = await res.json();

        const botMessage: Message = {
          id: Date.now().toString(),
          sender: 'bot',
          text: data.reply,
        };
        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Error communicating with backend:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        sender: 'bot',
        text: 'Error connecting to the backend.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSend();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedImage(e.target.files[0]);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Rescue AI</h1>
      </header>

      <main className="chat-container">
        <div className="messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-card ${msg.sender}`}>
              <div className="message-content">
                {msg.imageUrl && <img src={msg.imageUrl} alt="uploaded" className="uploaded-image" />}
                {msg.text && <p>{msg.text}</p>}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message-card bot">
              <div className="loading-state">Processing...</div>
            </div>
          )}
        </div>
      </main>

      <footer className="input-area">
        {selectedImage && (
          <div className="image-preview">
            <span>{selectedImage.name}</span>
            <button onClick={() => setSelectedImage(null)}>X</button>
          </div>
        )}
        <div className="input-box">
          <button className="upload-btn" onClick={() => fileInputRef.current?.click()}>📷</button>
          <input
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          <input
            type="text"
            placeholder="Type your message..."
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button className="send-btn" onClick={handleSend} disabled={isLoading}>Send</button>
        </div>
      </footer>
    </div>
  );
}

export default App;
