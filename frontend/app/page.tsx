"use client";

import { useRef, useState } from "react";

type UploadedDocument = {
  id: string;
  filename: string;
  file_type: string;
  locations_found: number;
  characters_extracted: number;
  chunks_created?: number;
  preview: string;
};

type Source = {
  source_number: number;
  document_id: string;
  filename: string;
  location: string;
  similarity: number;
  preview: string;
};

export default function Home() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [language, setLanguage] = useState<"en" | "ar">("en");
  const isArabic = language === "ar";

  const t = {
    en: {
      chatDocuments: "Chat with your documents",
      languageButton: "العربية",
      powered: "Powered locally by Ollama",
      badge: "AI-powered document assistant",
      title1: "Understand your documents",
      title2: "without reading them all.",
      description:
        "Upload your documents, get instant summaries, and ask questions in Arabic or English. DocMind answers using only the information inside your files.",

      uploadTitle: "Upload your documents",
      uploadDescription: "Drag and drop your files here, or click to browse",
      chooseFiles: "Choose files",
      selectedFiles: "Selected files",
      file: "file",
      files: "files",
      remove: "Remove",
      reading: "Reading your documents...",
      continueWith: "Continue with",

      processed: "Documents processed successfully",
      locations: "locations",
      characters: "characters",
      chunks: "chunks",
      ready: "Ready",
      preview: "Preview",

      askTitle: "Ask your documents",
      askDescription: "Ask in Arabic or English.",
      askPlaceholder: "Ask anything about your documents...",
      sendHint: "Enter to send • Shift + Enter for a new line",
      ask: "Ask",
      thinking: "Thinking...",
      sources: "Sources",
      match: "match",

      summaries: "Instant Summaries",
      summariesDesc:
        "Turn long documents into clear and useful summaries in seconds.",

      askFeature: "Ask Your Documents",
      askFeatureDesc:
        "Ask questions and receive answers grounded only in your uploaded files.",

      bilingual: "Arabic & English",
      bilingualDesc:
        "Ask in Arabic even when your documents are written in English, or the other way around.",

      uploadFirst: "Upload and process a document first.",
      uploadFailed: "Failed to upload files",
      uploadGenericError:
        "Something went wrong while processing your documents.",
      answerFailed: "Failed to answer the question",
      answerGenericError:
        "Something went wrong while answering your question.",

      footerBuiltBy: "Built by",
      footerName: "Ziyad Alghamdi",
      footerRights: "All rights reserved.",
      github: "GitHub",
      linkedin: "LinkedIn",
    },

    ar: {
      chatDocuments: "تحدث مع ملفاتك",
      languageButton: "English",
      powered: "يعمل محليًا باستخدام Ollama",
      badge: "مساعد ذكي لفهم المستندات",
      title1: "افهم ملفاتك",
      title2: "بدون الحاجة لقراءتها كلها.",
      description:
        "ارفع ملفاتك، واحصل على ملخصات سريعة، واسأل عنها بالعربية أو الإنجليزية. يجيب DocMind اعتمادًا على المعلومات الموجودة داخل ملفاتك فقط.",

      uploadTitle: "ارفع ملفاتك",
      uploadDescription: "اسحب الملفات هنا أو اضغط لاختيارها",
      chooseFiles: "اختيار الملفات",
      selectedFiles: "الملفات المختارة",
      file: "ملف",
      files: "ملفات",
      remove: "حذف",
      reading: "جاري قراءة الملفات...",
      continueWith: "متابعة باستخدام",

      processed: "تمت معالجة الملفات بنجاح",
      locations: "مواقع",
      characters: "حرف",
      chunks: "أجزاء",
      ready: "جاهز",
      preview: "معاينة",

      askTitle: "اسأل ملفاتك",
      askDescription: "اسأل بالعربية أو الإنجليزية.",
      askPlaceholder: "اكتب أي سؤال عن ملفاتك...",
      sendHint: "Enter للإرسال • Shift + Enter لسطر جديد",
      ask: "اسأل",
      thinking: "جاري التفكير...",
      sources: "المصادر",
      match: "تطابق",

      summaries: "تلخيص فوري",
      summariesDesc:
        "حوّل المستندات الطويلة إلى ملخصات واضحة ومفيدة خلال ثوانٍ.",

      askFeature: "اسأل ملفاتك",
      askFeatureDesc:
        "اسأل عن ملفاتك واحصل على إجابات مبنية على محتوى الملفات فقط.",

      bilingual: "العربية والإنجليزية",
      bilingualDesc:
        "اسأل بالعربية حتى لو كان الملف بالإنجليزية، أو العكس.",

      uploadFirst: "ارفع ملفًا وعالجه أولًا.",
      uploadFailed: "فشل رفع الملفات",
      uploadGenericError: "حدث خطأ أثناء معالجة الملفات.",
      answerFailed: "فشل الحصول على إجابة",
      answerGenericError: "حدث خطأ أثناء الإجابة عن سؤالك.",

      footerBuiltBy: "تم التطوير بواسطة",
      footerName: "زياد الغامدي",
      footerRights: "جميع الحقوق محفوظة.",
      github: "GitHub",
      linkedin: "LinkedIn",
    },
  }[language];

  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadedDocuments, setUploadedDocuments] = useState<
    UploadedDocument[]
  >([]);
  const [uploadError, setUploadError] = useState("");

  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [askError, setAskError] = useState("");

  function handleFiles(selectedFiles: FileList | null) {
    if (!selectedFiles) return;

    const newFiles = Array.from(selectedFiles);

    setFiles((currentFiles) => {
      const allFiles = [...currentFiles, ...newFiles];

      return allFiles.filter(
        (file, index, array) =>
          index ===
          array.findIndex(
            (item) => item.name === file.name && item.size === file.size
          )
      );
    });

    setUploadedDocuments([]);
    setUploadError("");
    setAnswer("");
    setSources([]);
    setAskError("");
  }

  function removeFile(indexToRemove: number) {
    setFiles((currentFiles) =>
      currentFiles.filter((_, index) => index !== indexToRemove)
    );

    setUploadedDocuments([]);
    setUploadError("");
    setAnswer("");
    setSources([]);
    setAskError("");
  }

  function formatFileSize(bytes: number) {
    if (bytes < 1024) return `${bytes} B`;

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  async function uploadFiles() {
    if (files.length === 0) return;

    setUploading(true);
    setUploadError("");
    setUploadedDocuments([]);
    setAnswer("");
    setSources([]);

    try {
      const formData = new FormData();

      files.forEach((file) => {
        formData.append("files", file);
      });

      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || t.uploadFailed);
      }

      setUploadedDocuments(data.documents);
    } catch (error) {
      setUploadError(
        error instanceof Error ? error.message : t.uploadGenericError
      );
    } finally {
      setUploading(false);
    }
  }

  async function askDocuments() {
    if (!question.trim()) return;

    if (uploadedDocuments.length === 0) {
      setAskError(t.uploadFirst);
      return;
    }

    setAsking(true);
    setAskError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
          document_ids: uploadedDocuments.map((document) => document.id),
          top_k: 5,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || t.answerFailed);
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setAskError(
        error instanceof Error ? error.message : t.answerGenericError
      );
    } finally {
      setAsking(false);
    }
  }

  function handleQuestionKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askDocuments();
    }
  }

  return (
    <main
      dir={isArabic ? "rtl" : "ltr"}
      lang={language}
      className="min-h-screen bg-[#f7f8fc] text-slate-900"
    >
      {/* Navbar */}
      <nav className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-lg font-bold text-white">
              D
            </div>

            <div>
              <h1 className="text-lg font-bold">DocMind AI</h1>
              <p className="text-xs text-slate-500">{t.chatDocuments}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="hidden text-xs text-slate-400 sm:block">
              {t.powered}
            </span>

            <button
              type="button"
              onClick={() =>
                setLanguage((current) => (current === "en" ? "ar" : "en"))
              }
              className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium transition hover:bg-slate-50"
            >
              {t.languageButton}
            </button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-5xl px-6 pb-10 pt-20 text-center">
        <div className="mb-5 inline-flex rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700">
          {t.badge}
        </div>

        <h2 className="mx-auto max-w-4xl text-4xl font-bold tracking-tight sm:text-6xl">
          {t.title1}
          <span className="text-indigo-600"> {t.title2}</span>
        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
          {t.description}
        </p>
      </section>

      {/* Upload Area */}
      <section className="mx-auto max-w-3xl px-6">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.docx,.pptx"
            className="hidden"
            onChange={(event) => handleFiles(event.target.files)}
          />

          <div
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault();
              handleFiles(event.dataTransfer.files);
            }}
            className="rounded-2xl border-2 border-dashed border-slate-300 px-6 py-14 text-center transition hover:border-indigo-400 hover:bg-indigo-50/30"
          >
            <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-100">
              <svg
                width="26"
                height="26"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="text-indigo-600"
              >
                <path d="M12 16V4" />
                <path d="m7 9 5-5 5 5" />
                <path d="M20 15v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-4" />
              </svg>
            </div>

            <h3 className="text-xl font-semibold">{t.uploadTitle}</h3>

            <p className="mt-2 text-sm text-slate-500">
              {t.uploadDescription}
            </p>

            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="mt-6 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-700"
            >
              {t.chooseFiles}
            </button>

            <p className="mt-4 text-xs text-slate-400">PDF • DOCX • PPTX</p>
          </div>

          {/* Selected Files */}
          {files.length > 0 && (
            <div className="mt-6">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="font-semibold">{t.selectedFiles}</h3>

                <span className="text-sm text-slate-500">
                  {files.length} {files.length === 1 ? t.file : t.files}
                </span>
              </div>

              <div className="space-y-3">
                {files.map((file, index) => (
                  <div
                    key={`${file.name}-${file.size}`}
                    className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
                  >
                    <div className="flex min-w-0 items-center gap-3">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-indigo-100 text-sm font-bold text-indigo-600">
                        {file.name.split(".").pop()?.toUpperCase()}
                      </div>

                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium">
                          {file.name}
                        </p>
                        <p className="text-xs text-slate-500">
                          {formatFileSize(file.size)}
                        </p>
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => removeFile(index)}
                      disabled={uploading}
                      className="rounded-lg px-3 py-2 text-sm text-slate-400 transition hover:bg-red-50 hover:text-red-500 disabled:opacity-50"
                    >
                      {t.remove}
                    </button>
                  </div>
                ))}
              </div>

              <button
                type="button"
                onClick={uploadFiles}
                disabled={uploading}
                className="mt-5 w-full rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {uploading
                  ? t.reading
                  : `${t.continueWith} ${files.length} ${
                      files.length === 1 ? t.file : t.files
                    }`}
              </button>

              {uploadError && (
                <div
                  dir="auto"
                  className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600"
                >
                  {uploadError}
                </div>
              )}

              {/* Processed Documents */}
              {uploadedDocuments.length > 0 && (
                <div className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-5">
                  <div className="flex items-center gap-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-green-700">
                      ✓
                    </div>

                    <h3 className="font-semibold text-green-800">
                      {t.processed}
                    </h3>
                  </div>

                  <div className="mt-4 space-y-3">
                    {uploadedDocuments.map((document) => (
                      <div
                        key={document.id}
                        className="rounded-xl border border-green-200 bg-white p-4"
                      >
                        <div className="flex items-start justify-between gap-4">
                          <div className="min-w-0">
                            <p
                              dir="auto"
                              className="truncate font-medium"
                            >
                              {document.filename}
                            </p>

                            <p className="mt-1 text-xs text-slate-500">
                              {document.file_type.toUpperCase()} •{" "}
                              {document.locations_found} {t.locations}
                              {document.chunks_created !== undefined &&
                                ` • ${document.chunks_created} ${t.chunks}`}{" "}
                              •{" "}
                              {document.characters_extracted.toLocaleString()}{" "}
                              {t.characters}
                            </p>
                          </div>

                          <span className="shrink-0 rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                            {t.ready}
                          </span>
                        </div>

                        {document.preview && (
                          <div className="mt-3 rounded-lg bg-slate-50 p-3">
                            <p className="text-xs font-medium text-slate-400">
                              {t.preview}
                            </p>

                            <p
                              dir="auto"
                              className="mt-1 line-clamp-3 text-sm leading-6 text-slate-600"
                            >
                              {document.preview}
                            </p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* Ask Your Documents */}
      {uploadedDocuments.length > 0 && (
        <section className="mx-auto max-w-3xl px-6 py-10">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-5">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-100 text-xl">
                  💬
                </div>

                <div>
                  <h2 className="text-xl font-bold">{t.askTitle}</h2>
                  <p className="text-sm text-slate-500">{t.askDescription}</p>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3">
              <textarea
                dir="auto"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={handleQuestionKeyDown}
                placeholder={t.askPlaceholder}
                rows={3}
                className="w-full resize-none bg-transparent p-2 text-sm outline-none placeholder:text-slate-400"
              />

              <div className="mt-2 flex items-center justify-between gap-4">
                <p className="text-xs text-slate-400">{t.sendHint}</p>

                <button
                  type="button"
                  onClick={askDocuments}
                  disabled={asking || !question.trim()}
                  className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {asking ? t.thinking : t.ask}
                </button>
              </div>
            </div>

            {askError && (
              <div
                dir="auto"
                className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600"
              >
                {askError}
              </div>
            )}

            {/* AI Answer */}
            {answer && (
              <div className="mt-6">
                <div className="rounded-2xl border border-indigo-100 bg-indigo-50/50 p-5">
                  <div className="mb-3 flex items-center gap-2">
                    <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-600 text-xs font-bold text-white">
                      D
                    </div>

                    <span className="text-sm font-semibold">DocMind AI</span>
                  </div>

                  <p
                    dir="auto"
                    className="whitespace-pre-wrap text-sm leading-7 text-slate-700"
                  >
                    {answer}
                  </p>
                </div>

                {/* Sources */}
                {sources.length > 0 && (
                  <div className="mt-5">
                    <h3 className="mb-3 text-sm font-semibold text-slate-700">
                      {t.sources}
                    </h3>

                    <div className="space-y-3">
                      {sources.map((source) => (
                        <div
                          key={`${source.filename}-${source.location}-${source.source_number}`}
                          className="rounded-xl border border-slate-200 bg-white p-4"
                        >
                          <div className="flex items-center justify-between gap-4">
                            <div className="min-w-0">
                              <p
                                dir="auto"
                                className="truncate text-sm font-medium"
                              >
                                [{source.source_number}] {source.filename}
                              </p>

                              <p className="mt-1 text-xs font-medium text-indigo-600">
                                {source.location}
                              </p>
                            </div>

                            <span className="shrink-0 rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-500">
                              {Math.round(source.similarity * 100)}% {t.match}
                            </span>
                          </div>

                          <p
                            dir="auto"
                            className="mt-3 line-clamp-3 text-xs leading-5 text-slate-500"
                          >
                            {source.preview}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Features */}
      <section className="mx-auto grid max-w-5xl gap-5 px-6 py-16 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="mb-4 text-2xl">✨</div>
          <h3 className="font-semibold">{t.summaries}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-500">
            {t.summariesDesc}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="mb-4 text-2xl">💬</div>
          <h3 className="font-semibold">{t.askFeature}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-500">
            {t.askFeatureDesc}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <div className="mb-4 text-2xl">🌐</div>
          <h3 className="font-semibold">{t.bilingual}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-500">
            {t.bilingualDesc}
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-6 border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-7 text-sm text-slate-500 sm:flex-row">
          <div className="text-center sm:text-start">
            <p>
              {t.footerBuiltBy}{" "}
              <span className="font-semibold text-slate-800">
                {t.footerName}
              </span>
            </p>

            <p className="mt-1 text-xs text-slate-400">
              © 2026 {t.footerName}. {t.footerRights}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <a
              href="https://github.com/ziyad-alghamdi"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-lg border border-slate-200 bg-white px-4 py-2 font-medium text-slate-700 transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
            >
              {t.github} ↗
            </a>

            <a
              href="https://www.linkedin.com/in/ziyad-alghamdi-a97366251"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-lg border border-slate-200 bg-white px-4 py-2 font-medium text-slate-700 transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
            >
              {t.linkedin} ↗
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}
