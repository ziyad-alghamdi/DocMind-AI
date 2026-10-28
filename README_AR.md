<p align="center">
  <a href="README.md">English</a> · <strong>العربية</strong>
</p>

<h1 align="center">DocMind AI</h1>

<p align="center">
  <strong>مساعد ذكي متعدد اللغات لفهم المستندات باستخدام Retrieval-Augmented Generation (RAG)</strong>
</p>

<p align="center">
  ارفع ملفاتك، اسأل بالعربية أو الإنجليزية، واحصل على إجابة مبنية على محتوى ملفاتك مع توضيح الملف والصفحة أو الشريحة أو الفقرة التي استندت إليها الإجابة.
</p>

<p align="center">
  <a href="https://docmind-ai-smoky.vercel.app"><strong>تجربة الموقع</strong></a> ·
  <a href="https://docmind-ai-api-k5f4.onrender.com/docs"><strong>توثيق الـAPI</strong></a> ·
  <a href="README.md"><strong>English README</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-Frontend-black?logo=nextdotjs" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-8E75B2?logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/Vercel-Frontend-black?logo=vercel" alt="Vercel" />
  <img src="https://img.shields.io/badge/Render-Backend-46E3B7?logo=render&logoColor=black" alt="Render" />
</p>

---

## نبذة عن المشروع

**DocMind AI** هو تطبيق Full-Stack ذكي متعدد اللغات صُمم لمساعدة المستخدم على فهم عدد كبير من الملفات بدون الحاجة إلى قراءة كل صفحة يدويًا.

بدل أن يعمل كـChatbot عام، يعتمد النظام على بنية **Retrieval-Augmented Generation (RAG)**. يقوم باستخراج النصوص من الملفات، تقسيمها إلى أجزاء قابلة للبحث، تحويلها إلى Embeddings دلالية، استرجاع الأجزاء الأكثر ارتباطًا بالسؤال، ثم إرسال هذا السياق فقط إلى نموذج الذكاء الاصطناعي للإجابة.

الهدف هو أن تكون الإجابة مرتبطة بمحتوى المستندات المحددة، مع إظهار المصدر الذي استندت إليه الإجابة، وذكر أن المعلومة غير موجودة عندما لا يتم العثور عليها في السياق المسترجع.

النسخة المنشورة تدعم **العربية والإنجليزية**، بما في ذلك البحث بين اللغات، مثل أن تسأل بالعربية عن معلومة موجودة داخل ملف إنجليزي.

---

## النسخة المنشورة

| الجزء | الرابط | الحالة |
| --- | --- | --- |
| الموقع | https://docmind-ai-smoky.vercel.app | متاح |
| Backend API | https://docmind-ai-api-k5f4.onrender.com | متاح |
| Swagger API Docs | https://docmind-ai-api-k5f4.onrender.com/docs | متاح |

> الـBackend يعمل حاليًا على Render Free Tier، لذلك قد يكون أول طلب بعد فترة من عدم الاستخدام أبطأ بينما تعود الخدمة للعمل.

---

## أهم الميزات

| الميزة | الوصف |
| --- | --- |
| **رفع عدة ملفات** | رفع ومعالجة ملف واحد أو عدة ملفات في الجلسة نفسها. |
| **دعم PDF** | استخراج النص مع الاحتفاظ برقم الصفحة كمصدر. |
| **دعم DOCX** | استخراج فقرات ملفات Word مع مواقعها. |
| **دعم PPTX** | استخراج النص من شرائح PowerPoint مع رقم الشريحة. |
| **واجهة عربية وإنجليزية** | التبديل بين اللغتين من داخل الموقع. |
| **سؤال بلغة وملف بلغة أخرى** | السؤال بالعربية عن ملف إنجليزي والعكس. |
| **بحث دلالي** | استخدام Embeddings متعددة اللغات بدل الاعتماد فقط على الكلمات المتطابقة. |
| **RAG** | استرجاع الأجزاء المهمة قبل إنشاء الإجابة. |
| **إجابات مقيدة بالمستندات** | تعليمات النموذج تطلب منه استخدام السياق المسترجع وعدم تخمين معلومات غير موجودة. |
| **مصادر داخل الإجابة** | دعم الاستشهاد بالمصادر باستخدام `[1]` و`[2]` وغيرها. |
| **تحديد مكان المعلومة** | إظهار اسم الملف والصفحة أو الفقرة أو الشريحة. |
| **Similarity Score** | نتائج البحث تحتوي على درجة تشابه دلالي. |
| **Intent Boosting** | تحسين بعض الاستعلامات المنظمة مثل الاسم والجامعة والبريد والجوال والمهارات والخبرات. |
| **تحديد الملفات المستخدمة** | البحث يقتصر على Document IDs التي يرسلها العميل الحالي. |
| **Summarization API** | الـBackend يحتوي endpoint باسم `/summarize` للتلخيص المبني على المستندات. |
| **Swagger Docs** | توثيق تفاعلي تلقائي للـAPI من FastAPI. |
| **Responsive UI** | يعمل من الجوال والكمبيوتر. |
| **لا يحتاج الزائر لتثبيت AI محلي** | المستخدم العام يحتاج فقط متصفحًا، لأن الذكاء الاصطناعي يعمل عبر الـBackend المنشور وGemini API. |

---

## كيف يعمل النظام؟

```text
PDF / DOCX / PPTX
        │
        ▼
   استخراج النص
        │
        ▼
تقسيم النص + بيانات المصدر
(ملف + صفحة/شريحة/فقرة)
        │
        ▼
 Gemini Embedding 2
        │
        ▼
 تخزين متجهات في الذاكرة
        │
        ▼
    سؤال المستخدم
        │
        ▼
 Embedding للسؤال
        │
        ▼
Cosine Similarity + Intent Boost
        │
        ▼
أكثر الأجزاء ارتباطًا
        │
        ▼
 Gemini 3.8 Flash
        │
        ▼
 إجابة مقيدة + مصادر
```

### 1. قراءة الملفات

يستقبل FastAPI Backend الملفات التالية:

- `.pdf`
- `.docx`
- `.pptx`

ويستخدم:

- **PyPDF** لملفات PDF
- **python-docx** لملفات Word
- **python-pptx** لملفات PowerPoint

### 2. حفظ معلومات المصدر

أثناء استخراج النص يحفظ النظام موقع المعلومة:

- PDF → `Page X`
- DOCX → `Paragraph X`
- PPTX → `Slide X`

وتستمر هذه البيانات مع الـChunk حتى يمكن إظهار المصدر للمستخدم.

### 3. تقسيم النص

يتم تقسيم المحتوى الطويل إلى Chunks متداخلة، مع محاولة التقسيم عند حدود طبيعية مثل نهاية السطر ونهاية الجملة وعلامات الترقيم العربية والإنجليزية.

### 4. Embeddings

يتم تحويل كل Chunk إلى تمثيل رقمي دلالي باستخدام **Gemini Embedding 2** (`gemini-embedding-2`).

التنفيذ الحالي يطلب **768-dimensional embeddings**.

### 5. الاسترجاع

عند طرح سؤال:

1. يتم إنشاء Embedding للسؤال؛
2. يتم حساب Cosine Similarity مع Chunks المخزنة؛
3. يمكن إضافة Intent Boost بسيط لبعض الحقول المنظمة؛
4. يتم ترتيب النتائج؛
5. يتم إرسال أفضل الأجزاء فقط إلى نموذج الإجابة.

### 6. إنشاء الإجابة

يتم إرسال السياق المسترجع إلى **Gemini 3.8 Flash** (`gemini-3.8-flash`).

تعليمات النظام تطلب من النموذج:

- استخدام السياق المسترجع فقط؛
- عدم تخمين المعلومات المفقودة؛
- المحافظة على الأسماء والبريد والأرقام والمعرفات والتواريخ كما هي؛
- الإجابة بنفس لغة سؤال المستخدم بشكل افتراضي؛
- الاستشهاد بالمصادر؛
- ذكر أن المعلومة غير موجودة إذا لم يتم العثور عليها.

---

## دعم العربية والإنجليزية

دعم اللغات لا يقتصر على ترجمة الواجهة.

إذا كان الملف يحتوي على:

```text
University: King Abdulaziz University
```

يمكن للمستخدم أن يسأل:

```text
ما هي الجامعة؟
```

ويستطيع DocMind استرجاع المحتوى الإنجليزي دلاليًا ثم الإجابة بالعربية مع المحافظة على القيمة الأصلية.

ويعمل الاتجاه العكسي أيضًا: يمكن للسؤال الإنجليزي استرجاع محتوى عربي مناسب.

---

## الإجابات مع المصدر

مثال:

```text
السؤال:
ما هي الجامعة؟

الإجابة:
King Abdulaziz University. [1]

المصدر [1]:
الملف: (CV) ZIYAD Alghamdi.pdf
الموقع: Page 1
```

كما تعرض الواجهة Preview من النص المسترجع حتى يستطيع المستخدم مقارنة الإجابة بالسياق الأصلي.

---

## الأدوات والتقنيات

### Frontend

| التقنية | الاستخدام |
| --- | --- |
| **Next.js** | إطار تطبيق الويب |
| **React** | واجهة المستخدم وإدارة الحالة |
| **TypeScript** | تطوير Frontend بأنواع بيانات واضحة |
| **Tailwind CSS** | تصميم Responsive |
| **Vercel** | استضافة الواجهة والنشر |

### Backend

| التقنية | الاستخدام |
| --- | --- |
| **Python** | لغة الـBackend ومعالجة المستندات |
| **FastAPI** | REST API |
| **Uvicorn** | تشغيل ASGI |
| **HTTPX** | الاتصال بـGemini API |
| **NumPy** | عمليات المتجهات وCosine Similarity |
| **PyPDF** | استخراج PDF |
| **python-docx** | استخراج DOCX |
| **python-pptx** | استخراج PPTX |
| **Render** | استضافة الـBackend |

### AI & Retrieval

| التقنية | الاستخدام |
| --- | --- |
| **Gemini 3.8 Flash** | إنشاء الإجابات والتلخيص |
| **Gemini Embedding 2** | Embeddings دلالية متعددة اللغات |
| **RAG** | ربط الإجابة بمحتوى الملفات المسترجع |
| **Cosine Similarity** | ترتيب الأجزاء حسب الارتباط بالسؤال |
| **Intent Boosting** | تحسين بعض عمليات الاسترجاع المنظمة |

---

## معمارية النظام

```text
┌──────────────────────────┐
│     المستخدم / المتصفح   │
│      جوال أو كمبيوتر      │
└─────────────┬────────────┘
              │ HTTPS
              ▼
┌──────────────────────────┐
│      Next.js Frontend    │
│          Vercel          │
└─────────────┬────────────┘
              │ REST API
              ▼
┌──────────────────────────┐
│      FastAPI Backend     │
│          Render          │
├──────────────────────────┤
│ استخراج المستندات        │
│ تقسيم النصوص             │
│ تخزين Embeddings         │
│ Semantic Retrieval       │
│ ربط المصادر              │
└─────────────┬────────────┘
              │ Gemini API
              ▼
┌──────────────────────────┐
│      Google Gemini       │
│  gemini-embedding-2      │
│  gemini-3.8-flash        │
└──────────────────────────┘
```

---

## API Endpoints

| Method | Endpoint | الاستخدام |
| --- | --- | --- |
| `GET` | `/` | معلومات الـAPI |
| `GET` | `/health` | التحقق من حالة الخدمة وإعداد AI |
| `POST` | `/upload` | استخراج الملفات وتقسيمها وإنشاء Embeddings |
| `POST` | `/search` | استرجاع الأجزاء الأكثر ارتباطًا دلاليًا |
| `POST` | `/ask` | الإجابة من سياق الملفات المسترجع |
| `POST` | `/summarize` | إنشاء ملخص مبني على المستندات |

التوثيق التفاعلي:

**https://docmind-ai-api-k5f4.onrender.com/docs**

---

## هيكلة المشروع

```text
DocMind-AI/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── .gitignore
├── render.yaml
├── README.md
└── README_AR.md
```

---

## النشر

### Frontend — Vercel

واجهة Next.js منشورة على Vercel.

```env
NEXT_PUBLIC_API_URL=https://docmind-ai-api-k5f4.onrender.com
```

### Backend — Render

FastAPI منشور كـRender Web Service.

المفتاح السري المطلوب:

```env
GEMINI_API_KEY=your_gemini_api_key
```

ويتم ضبط CORS باستخدام:

```env
ALLOWED_ORIGINS=https://docmind-ai-smoky.vercel.app
```

مفتاح Gemini محفوظ في الـBackend ولا يتم تضمينه داخل كود المتصفح أو رفعه إلى GitHub.

---

## تشغيل المشروع محليًا

### المتطلبات

- Git
- Node.js
- Python
- Gemini API Key

### 1. تحميل المشروع

```bash
git clone https://github.com/ziyad-alghamdi/DocMind-AI.git
cd DocMind-AI
```

### 2. تشغيل Backend

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

تثبيت الحزم:

```bash
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
$env:ALLOWED_ORIGINS="http://localhost:3000"
```

macOS / Linux:

```bash
export GEMINI_API_KEY="YOUR_KEY"
export ALLOWED_ORIGINS="http://localhost:3000"
```

تشغيل الـBackend:

```bash
uvicorn main:app --reload
```

API: `http://localhost:8000`

Swagger: `http://localhost:8000/docs`

### 3. تشغيل Frontend

افتح Terminal جديد:

```bash
cd frontend
npm install
```

أنشئ `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

ثم:

```bash
npm run dev
```

افتح `http://localhost:3000`.

---

## تحميل المشروع

يمكن تحميل Source Code من GitHub عن طريق:

**GitHub → Code → Download ZIP**

أو:

```bash
git clone https://github.com/ziyad-alghamdi/DocMind-AI.git
```

---

## الأمان والخصوصية

- Gemini API Key محفوظ كمتغير بيئة في الـBackend.
- المفتاح وملفات `.env` غير مرفوعة إلى GitHub.
- الـVirtual Environment ومجلدات البناء المحلية مستبعدة.
- نصوص المستندات المرفوعة تتم معالجتها في الـBackend، ويتم إرسال المحتوى المطلوب إلى Gemini API لإنشاء Embeddings والإجابات.
- النسخة الحالية تخزن المستندات المعالجة والـEmbeddings **في ذاكرة السيرفر** وليس في قاعدة بيانات دائمة.
- البيانات الموجودة في الذاكرة تختفي عند إعادة تشغيل أو إعادة نشر خدمة Render.
- النسخة الحالية لا تحتوي على تسجيل دخول أو تخزين دائم للمستندات الشخصية.

---

## حدود النسخة الحالية

المشروع الحالي Prototype / Portfolio يعمل فعليًا، لكنه ليس منصة إدارة مستندات Production كاملة.

الحدود الحالية:

- ملفات PDF الممسوحة كصور لا تحتوي بعد على OCR؛
- الحد الأقصى الحالي لحجم الملف هو **10 MB لكل ملف**؛
- المستندات والـEmbeddings مخزنة في الذاكرة؛
- لا توجد Vector Database دائمة؛
- لا توجد حسابات مستخدمين أو Chat History دائم؛
- Render Free Tier قد يجعل أول طلب أبطأ بعد فترة من عدم الاستخدام؛
- الـBackend يحتوي على Summarization Endpoint، بينما تركز الواجهة العامة الحالية بشكل أساسي على رفع الملفات والأسئلة والأجوبة.

---

## التطوير المستقبلي

- OCR للملفات الممسوحة والصور
- Vector Database دائمة
- تسجيل دخول المستخدمين
- Workspaces خاصة
- Chat History دائم
- حذف المستندات وإدارة دورة حياتها
- Streaming للإجابات
- Reranking أقوى
- Background Jobs لمعالجة الملفات
- Progress Indicators
- دعم صيغ إضافية
- تقييم آلي لجودة RAG
- Rate Limiting وصلاحيات وصول أقوى
- Custom Domain
- اختبارات آلية وCI/CD

---

## ماذا يوضح هذا المشروع تقنيًا؟

DocMind AI يوضح تطبيقًا عمليًا لـ:

- Full-Stack AI Development
- Retrieval-Augmented Generation
- Semantic Vector Search
- Multilingual Embeddings
- Prompt Grounding وAnti-Hallucination Constraints
- Source Attribution
- Document Parsing
- REST API Design
- Frontend / Backend Integration
- Secret Management
- Cloud Deployment باستخدام Vercel وRender

---

## المطور

**Ziyad Alghamdi**

- GitHub: https://github.com/ziyad-alghamdi
- LinkedIn: https://www.linkedin.com/in/ziyad-alghamdi-a97366251
- المشروع: https://github.com/ziyad-alghamdi/DocMind-AI
- Live Demo: https://docmind-ai-smoky.vercel.app

---

## الحقوق

© 2026 Ziyad Alghamdi. جميع الحقوق محفوظة.

المستودع متاح للعامة ويمكن استعراضه وتحميله من GitHub. لا يوجد حاليًا ملف License منفصل يمنح ترخيصًا مفتوح المصدر ما لم تتم إضافته لاحقًا.