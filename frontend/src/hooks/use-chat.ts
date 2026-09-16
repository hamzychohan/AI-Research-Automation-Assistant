"use client";

import { useState, useEffect, useRef } from "react";
import { useAuth } from "./use-auth";

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  created_at?: string;
}

interface ChatSession {
  id: string;
  title: string;
  created_at: string;
}

interface ActiveTool {
  name: string;
  status: "executing" | "completed";
  input?: string;
}

export function useChat() {
  const { token } = useAuth();
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [activeTool, setActiveTool] = useState<ActiveTool | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  // 1. Fetch all previous chat sessions
  const loadSessions = async () => {
    if (!token) return;
    try {
      const res = await fetch("http://localhost:8000/api/v1/chat/sessions", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setSessions(data);
        if (data.length > 0 && !currentSessionId) {
          setCurrentSessionId(data[0].id);
        }
      }
    } catch (err) {
      console.error("Failed to load sessions:", err);
    }
  };

  // 2. Create a new chat session
  const createSession = async (title: string = "New Chat Session") => {
    if (!token) return null;
    try {
      const res = await fetch("http://localhost:8000/api/v1/chat/sessions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ title })
      });
      if (res.ok) {
        const data = await res.json();
        setSessions(prev => [data, ...prev]);
        setCurrentSessionId(data.id);
        setMessages([]);
        return data.id;
      }
    } catch (err) {
      console.error("Failed to create session:", err);
    }
    return null;
  };

  // 3. Load historical messages for a session
  const loadMessages = async (sessionId: string) => {
    if (!token) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/chat/sessions/${sessionId}/messages`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
      }
    } catch (err) {
      console.error("Failed to load messages:", err);
    }
  };

  // Trigger loading history when active session changes
  useEffect(() => {
    if (currentSessionId) {
      loadMessages(currentSessionId);
    }
  }, [currentSessionId]);

  // Load sessions list on startup
  useEffect(() => {
    if (token) {
      loadSessions();
    }
  }, [token]);

  // 4. WebSocket stream management
  useEffect(() => {
    if (!currentSessionId || !token) return;

    const wsUrl = `ws://localhost:8000/api/v1/chat/ws/assistant/${currentSessionId}?token=${token}`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WebSocket assistant connection active.");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "token") {
        setIsLoading(false);
        setMessages(prev => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            // Append incoming character token to active reply bubble
            return [
              ...prev.slice(0, -1),
              { ...lastMsg, content: lastMsg.content + data.token }
            ];
          } else {
            // Instantiate fresh reply bubble
            return [
              ...prev,
              { id: Math.random().toString(), role: "assistant", content: data.token }
            ];
          }
        });
      } 
      
      else if (data.type === "tool_start") {
        setActiveTool({
          name: data.tool,
          status: "executing",
          input: data.input
        });
      } 
      
      else if (data.type === "tool_end") {
        setActiveTool({
          name: data.tool,
          status: "completed",
          input: data.input
        });
        // Retain check bubble for brief review before clearing
        setTimeout(() => {
          setActiveTool(null);
        }, 3000);
      } 
      
      else if (data.type === "title_update") {
        setSessions(prev =>
          prev.map(s => (s.id === currentSessionId ? { ...s, title: data.title } : s))
        );
      } 
      
      else if (data.type === "error") {
        setIsLoading(false);
        alert(data.message);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket assistant connection closed.");
      setIsLoading(false);
    };

    return () => {
      socket.close();
    };
  }, [currentSessionId, token]);

  // 5. Send message trigger
  const sendMessage = (content: string) => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      alert("Socket is currently disconnected. Reconnecting...");
      return;
    }

    // Append user message immediately to the message frame list
    const userMsg: Message = {
      id: Math.random().toString(),
      role: "user",
      content,
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);
    
    socketRef.current.send(JSON.stringify({ content }));
  };

  return {
    sessions,
    currentSessionId,
    setCurrentSessionId,
    messages,
    activeTool,
    isLoading,
    createSession,
    sendMessage,
    loadSessions
  };
}
