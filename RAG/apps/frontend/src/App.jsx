import { useState, useRef, useEffect } from 'react';
import { UploadCloud, FileText, Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);

  const messagesEndRef = useRef(null);

  // Auto-scroll chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle Drag & Drop / File Selection
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUploadSubmit = async () => {
    if (!file) return;
    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', file);
    if (sessionId) formData.append('session_id', sessionId);

    try {
      const res = await fetch('http://localhost:8001/upload', {
        method: 'POST',
        body: formData,
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Upload failed');
      
      setSessionId(data.session_id);
      setMessages(prev => [...prev, {
        role: 'ai',
        text: `Successfully ingested **${data.source_file}** into the RAG engine. Created ${data.chunks_ingested} vector chunks.`
      }]);
      setFile(null);
    } catch (err) {
      alert(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  // Handle Query Execution
  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputMsg.trim() || !sessionId) return;

    const query = inputMsg.trim();
    setInputMsg('');
    setMessages(prev => [...prev, { role: 'user', text: query }]);
    setIsQuerying(true);

    try {
      const res = await fetch('http://localhost:8001/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          question: query
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Query failed');

      setMessages(prev => [...prev, { role: 'ai', text: data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: `Error: ${err.message}` }]);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <>
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>
      
      <div className="app-container">
        
        {/* LEFT SIDEBAR - INGESTION */}
        <div className="panel sidebar">
          <div className="brand">
            <Sparkles strokeWidth={2.5} /> RAG Engine
          </div>
          
          <div className="upload-zone">
            <input 
              type="file" 
              accept=".pdf" 
              onChange={handleFileChange} 
              disabled={isUploading} 
            />
            {file ? (
              <>
                <FileText className="upload-icon" />
                <h3>Ready to Ingest</h3>
                <span className="file-info">{file.name} ({Math.round(file.size/1024)} KB)</span>
              </>
            ) : (
              <>
                <UploadCloud className="upload-icon" />
                <h3>Drop your PDF here</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '8px' }}>
                  Click or drag and drop to upload
                </p>
              </>
            )}
          </div>

          <button 
            className="submit-btn" 
            onClick={handleUploadSubmit}
            disabled={!file || isUploading}
          >
            {isUploading ? (
              <><Loader2 className="spinner" size={20} /> Ingesting Vector Chunks...</>
            ) : (
              <><span style={{fontWeight: 700}}>+</span> Process Document</>
            )}
          </button>
        </div>

        {/* RIGHT AREA - RAG CHAT */}
        <div className="panel chat-area">
          <div className="chat-header">
            <h2>Document Intelligence</h2>
            <div className="status-badge">
              <span className={`status-dot ${sessionId ? 'active' : ''}`}></span>
              {sessionId ? 'Session Active' : 'Awaiting Context'}
            </div>
          </div>

          <div className="messages">
            {messages.length === 0 ? (
              <div className="empty-state">
                <Bot strokeWidth={1} />
                <h2>AI Assistant Ready</h2>
                <p>Upload a PDF document on the left to initialize the Vector Database and begin querying context.</p>
              </div>
            ) : (
              messages.map((m, i) => (
                <div key={i} className={`msg ${m.role}`}>
                  <div className="avatar">
                    {m.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                  </div>
                  <div className="bubble">
                    {m.text}
                  </div>
                </div>
              ))
            )}
            
            {isQuerying && (
              <div className="msg ai">
                <div className="avatar"><Bot size={20}/></div>
                <div className="bubble" style={{display: 'flex', gap: '8px', alignItems: 'center'}}>
                 <Loader2 size={16} className="spinner"/> Generating response via Groq...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="input-area" onSubmit={handleSend}>
            <div className="input-box">
              <input 
                type="text" 
                placeholder={sessionId ? "Ask a question about your documents..." : "Upload a document to enable querying"}
                value={inputMsg}
                onChange={(e) => setInputMsg(e.target.value)}
                disabled={!sessionId || isQuerying}
              />
              <button type="submit" className="send-btn" disabled={!inputMsg.trim() || !sessionId || isQuerying}>
                <Send size={18} />
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default App;
