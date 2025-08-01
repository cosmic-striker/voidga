const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");
const svgCaptcha = require("svg-captcha");
const base64url = require("base64url");
const fs = require("fs");
const path = require("path");
const session = require("express-session");
const app = express();
const db = new sqlite3.Database("./db/database.sqlite3");

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(
  session({
    secret: "3e4f6b2a0c5e8d47e1fa9b4c2d6f8a9c7b3d2e5c1a9f0b6d5c7e2a3f4b1c6d8e",
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false },
  })
);

let currentCaptchaText = "";

// Route: GET /
app.get("/", (req, res) => {
  res.render("index", { error: null });
});

// Route: GET /captcha
app.get("/captcha", (req, res) => {
  try {
    const captcha = svgCaptcha.create({ size: 6, noise: 2 });
    req.session.captcha = captcha.text;
    // console.log(currentCaptchaText);

    // Save captcha as SVG file
    fs.writeFileSync(
      path.join(__dirname, "public", "captcha.svg"),
      captcha.data
    );

    const b64 = base64url.encode(base64url.encode(captcha.text));
    res.json({ success: true, b64});
  } catch (err) {
    console.error("CAPTCHA error:", err);
    res.status(500).send("Captcha generation failed.");
  }
});

// Route: POST /login
app.post("/login", (req, res) => {
  const { username, password, captcha } = req.body;

  if (!captcha || captcha !== req.session.captcha) {
    return res.render("index", { error: "CAPTCHA incorrect." });
  }
  req.session.captcha = null;

  //   const filtered =
  //     password.includes("select") ||
  //     password.includes(" ") ||
  //     password.includes("or") ||
  //     password.includes("and") ||
  //     password.includes("AND") ||
  //     password.includes("SELECT") ||
  //     password.includes("OR") ||
  //     password.includes("Select") ||
  //     password.includes("FROM") ||
  //     password.includes("from") ||
  //     password.includes("sElEcT") ||
  //     password.includes("SeLeCt");

  //   if (filtered) {
  //     return res.render("index", { error: "Suspicious input detected." });
  //   }

  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

  db.get(query, [], (err, row) => {
    if (err) return res.render("index", { error: "Internal Server Error." });

    if (row) {
      //   db.get("SELECT flag FROM flags LIMIT 1", (err, flagRow) => {
      return res.send(`
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: #111;
                font-family: sans-serif;
                color: #0f0;
                text-align: center;
                flex-direction: column;
            ">
                <h2 style="font-size: 2rem;">✅ Login Success</h2>
                <p style="font-size: 1.2rem; max-width: 600px;">
                Cyberhunter has some health issues 🤒🛌. So he can't develop further right now.
                </p>
            </div>
        `);

      //   });
    } else {
      res.render("index", { error: "Login failed." });
    }
  });
});

// Start the server
const PORT = 7777;
app.listen(PORT, () => {
  console.log(`🚀 SeeNoEvil running on http://localhost:${PORT}`);
});
