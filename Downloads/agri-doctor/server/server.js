import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import fetch from "node-fetch";

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());

app.post("/api/chat", async (req, res) => {
  try {
    const { message, language } = req.body;

    const prompt = `
You are Agri Doctor Assistant.
Answer ONLY in ${language}.
User question: "${message}"
`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
        }),
      }
    );

    const data = await response.json();
    const reply = data.candidates?.[0]?.content?.parts?.[0]?.text;

    res.json({ reply });
  } catch (err) {
    res.status(500).json({ error: "AI error" });
  }
});

app.listen(3000, () =>
  console.log("✅ Server running on http://localhost:3000")
);
