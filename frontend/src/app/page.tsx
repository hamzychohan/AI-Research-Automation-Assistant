"use client";

import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "@/hooks/use-auth";
import { useChat } from "@/hooks/use-chat";
import { 
  MessageSquare, Plus, LogOut, Send, Loader, Sparkles, 
  User, Lock, Mail, Cpu, Search, Slack, FileText, CheckCircle2 
} from "lucide-react";  
import loginStyles from "@/styles/login.module.css"; 
import chatStyles from "@/styles/chat.module.css";
import { marked } from "marked";

// Sub-component: Login/Registration interface
function LoginCard() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password);
        await login(email, password);
      }
    } catch (err: any) {
      setError(err.message || "An authentication error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
      <div className={loginStyles.loginContainer}>
      <div className={loginStyles.loginCard}>
        <div className={loginStyles.headerSection}>
          <div className={loginStyles.logoIcon}>
            <Cpu size={24} />
          </div>
          <h2 className={loginStyles.title}>
            {isLogin ? "Welcome Back" : "Create Account"}
          </h2>
          <p className={loginStyles.subtitle}>
            AI Research & Automation Assistant
          </p>
        </div>

        {error && (
          <div className={loginStyles.errorBanner}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className={loginStyles.form}>
          <div className={loginStyles.formGroup}>
            <label className={loginStyles.label}>Email Address</label>
            <div className={loginStyles.inputWrapper}>
              <Mail size={16} className={loginStyles.inputIcon} />
              <input 
                type="email"
                required
                className={loginStyles.input}
                placeholder="you@domain.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className={loginStyles.formGroup}>
            <label className={loginStyles.label}>Password</label>
            <div className={loginStyles.inputWrapper}>
              <Lock size={16} className={loginStyles.inputIcon} />
              <input 
                type="password"
                required
                className={loginStyles.input}
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button 
            type="submit" 
            className={loginStyles.submitButton}
            disabled={loading}
          >
            {loading ? "Processing..." : isLogin ? "Sign In" : "Register"}
          </button>
        </form>

        <div className={loginStyles.toggleContainer}>
          <span className={loginStyles.toggleText}>
            {isLogin ? "New to the platform?" : "Already have an account?"}
          </span>
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className={loginStyles.toggleButton}
          >
            {isLogin ? "Create account" : "Sign in instead"}
          </button>
        </div>
      </div>
    </div>
  );
}

// Sub-component: Chat Message item parsing Markdown
function ChatBubble({ role, content, createdAt }: { role: "user" | "assistant" | "system"; content: string; createdAt?: string }) {
  const [htmlContent, setHtmlContent] = useState("");

  useEffect(() => {
    const parseMarkdown = async () => {
      if (content) {
        try {
          const parsed = await marked.parse(content, { gfm: true, breaks: true });
          setHtmlContent(parsed);
        } catch (err) {
          setHtmlContent(content);
        }
      }
    };
    parseMarkdown();
  }, [content]);

  const formatTime = (timeStr?: string) => {
    if (!timeStr) return "";
    try {
      const date = new Date(timeStr);
      return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } catch {
      return "";
    }
  };

  const isUser = role === "user";

  return (
    <div className={`${chatStyles.messageBubble} ${isUser ? chatStyles.userBubble : chatStyles.aiBubble}`}>
      <div className={chatStyles.metaText}>
        {isUser ? "You" : "Assistant"} {createdAt ? `• ${formatTime(createdAt)}` : ""}
      </div>
      <div 
        className={chatStyles.messageText}
        dangerouslySetInnerHTML={{ __html: htmlContent || content }}
      />
    </div>
  );
}

// Sub-component: Tool Status visualizer card
function ToolStatusWidget({ name, status, input }: { name: string; status: "executing" | "completed"; input?: string }) {
  const isExecuting = status === "executing";

  const getToolIcon = () => {
    switch (name) {
      case "web_search":
        return <Search size={14} />;
      case "send_slack_notification":
        return <Slack size={14} />;
      case "create_gmail_draft":
        return <Mail size={14} />;
      case "save_research_report":
        return <FileText size={14} />;
      default:
        return <Cpu size={14} />;
    }
  };

  const getFriendlyName = () => {
    switch (name) {
      case "web_search":
        return "Web Search (Tavily)";
      case "send_slack_notification":
        return "Slack Notice (Placeholder)";
      case "create_gmail_draft":
        return "Gmail Draft (Placeholder)";
      case "save_research_report":
        return "Report Compiler";
      default:
        return name;
    }
  };

  return (
    <div className={`${chatStyles.toolStatusCard} ${isExecuting ? chatStyles.toolExecuting : chatStyles.toolCompleted}`}>
      <div className={chatStyles.toolHeader}>
        {isExecuting ? (
          <Loader size={12} className={chatStyles.spinner} />
        ) : (
          <CheckCircle2 size={12} />
        )}
        <span>{getFriendlyName()}</span>
        <span style={{ fontSize: "0.75rem", opacity: 0.8 }}>
          {isExecuting ? "Executing..." : "Finished"}
        </span>
      </div>
      {input && (
        <div className={chatStyles.toolInputs}>
          Args: {typeof input === "string" ? input : JSON.stringify(input)}
        </div>
      )}
    </div>
  );
}

// Sub-component: Workspace dashboard panel
function ChatWorkspace() {
  const { user, logout } = useAuth();
  const {
    sessions,
    currentSessionId,
    setCurrentSessionId,
    messages,
    activeTool,
    isLoading,
    createSession,
    sendMessage
  } = useChat();

  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  // Keep chat scrolled to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, activeTool]);

  const handleNewSession = async () => {
    await createSession("New Chat Session");
  };

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput("");
  };

  const activeSession = sessions.find(s => s.id === currentSessionId);

  return (
    <div className={chatStyles.workspaceLayout}>
      {/* Left Session Sidebar */}
      <aside className={chatStyles.sidebarPanel}>
        <div className={chatStyles.brandSection}>
          <Cpu size={22} />
          <span>Research AI</span>
        </div>

        <button onClick={handleNewSession} className={chatStyles.newSessionBtn}>
          <Plus size={16} />
          <span>New Chat</span>
        </button>

        <div className={chatStyles.sessionsList}>
          {sessions.map(s => {
            const isActive = s.id === currentSessionId;
            return (
              <button
                key={s.id}
                onClick={() => setCurrentSessionId(s.id)}
                className={`${chatStyles.sessionBtn} ${isActive ? chatStyles.activeSessionBtn : ""}`}
              >
                <MessageSquare size={14} />
                <span className={chatStyles.sessionTitle}>{s.title}</span>
              </button>
            );
          })}
        </div>

        <div className={chatStyles.logoutSection}>
          <button onClick={logout} className={chatStyles.logoutBtn}>
            <LogOut size={16} />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Right Chat Viewport */}
      <main className={chatStyles.chatViewport}>
        <header className={chatStyles.navbarHeader}>
          <h2 className={chatStyles.navbarTitle}>
            {activeSession ? activeSession.title : "Workspace"}
          </h2>
          <div className={chatStyles.userBadge}>
            <div className={chatStyles.userAvatar}>
              <User size={14} />
            </div>
            <span className={chatStyles.userEmail}>{user?.email}</span>
          </div>
        </header>

        {/* Messages list panel */}
        <div ref={scrollRef} className={chatStyles.messagesContainer}>
          {!currentSessionId ? (
            <div className={chatStyles.emptyState}>
              <Sparkles size={36} color="#6366f1" />
              <h3 className={chatStyles.emptyTitle}>AI Automation Assistant</h3>
              <p className={chatStyles.emptyDesc}>
                Open a previous chat thread or click 'New Chat' to perform Tavily research tasks, write reports, or trigger integration actions.
              </p>
            </div>
          ) : messages.length === 0 ? (
            <div className={chatStyles.emptyState}>
              <MessageSquare size={32} color="#8b5cf6" />
              <h3 className={chatStyles.emptyTitle}>New Chat Started</h3>
              <p className={chatStyles.emptyDesc}>
                Ask a research query, compile reports, or request notifications.
              </p>
            </div>
          ) : (
            messages.map(msg => (
              <ChatBubble 
                key={msg.id}
                role={msg.role}
                content={msg.content}
                createdAt={msg.created_at}
              />
            ))
          )}

          {/* Active Tool Loader */}
          {activeTool && (
            <ToolStatusWidget 
              name={activeTool.name}
              status={activeTool.status}
              input={activeTool.input}
            />
          )}
        </div>

        {/* Message Input Footer Form */}
        <form onSubmit={handleSend} className={chatStyles.inputForm}>
          <input 
            type="text"
            className={chatStyles.chatInput}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={currentSessionId ? "Ask a research question or request a task..." : "Select or start a chat session first"}
            disabled={!currentSessionId || isLoading}
          />
          <button 
            type="submit" 
            className={chatStyles.sendBtn}
            disabled={!currentSessionId || isLoading || !input.trim()}
          >
            <Send size={16} />
          </button>
        </form>
      </main>
    </div>
  );
}

// Master Entry Component
export default function HomePage() {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <div 
        style={{
          display: "flex",
          height: "100vh",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#0b0d10",
          color: "#9ca3af",
          fontFamily: "'Outfit', sans-serif"
        }}
      >
        <Loader size={24} className={chatStyles.spinner} style={{ marginRight: "10px" }} />
        <span>Loading AI Assistant...</span>
      </div>
    );
  }

  return token ? <ChatWorkspace /> : <LoginCard />;
}
