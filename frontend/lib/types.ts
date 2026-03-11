export type Session = {
  id: string;
  title: string;
  created_at: string;
};

export type ImageAttachment = {
  media_type: string;
  data: string;
  preview_url?: string;
};

export type Message = {
  role: "user" | "assistant";
  content: string;
  created_at: string;
  images?: ImageAttachment[];
};

export type QAPair = {
  user: Message;
  assistant: Message | null;
};
