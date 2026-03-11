"use client";

import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark, coldarkCold } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useTheme } from "@/lib/themeContext";

export default function MessageContent({ content }: { content: string }) {
  const { theme } = useTheme();
  const codeStyle = theme === "dark" ? oneDark : coldarkCold;

  return (
    <ReactMarkdown
      components={{
        code({ className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || "");
          const isInline = !match;
          return isInline ? (
            <code
              className="bg-code-bg text-code-text px-1 py-0.5 rounded text-sm font-mono"
              {...props}
            >
              {children}
            </code>
          ) : (
            <SyntaxHighlighter
              style={codeStyle}
              language={match[1]}
              PreTag="div"
              className="rounded-lg text-sm my-2"
              customStyle={{ overflowX: "auto", maxWidth: "100%" }}
            >
              {String(children).replace(/\n$/, "")}
            </SyntaxHighlighter>
          );
        },
        p({ children }) {
          return <p className="mb-3 last:mb-0 leading-relaxed">{children}</p>;
        },
        ul({ children }) {
          return <ul className="list-disc pl-5 mb-3 space-y-1">{children}</ul>;
        },
        ol({ children }) {
          return <ol className="list-decimal pl-5 mb-3 space-y-1">{children}</ol>;
        },
        h1({ children }) {
          return <h1 className="text-xl font-semibold mb-2 mt-4">{children}</h1>;
        },
        h2({ children }) {
          return <h2 className="text-lg font-semibold mb-2 mt-4">{children}</h2>;
        },
        h3({ children }) {
          return <h3 className="text-base font-semibold mb-1 mt-3">{children}</h3>;
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
