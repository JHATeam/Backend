import express from "express";
import cors from "cors";
import { PORT } from "./config.js";
import authRoutes from "./routes/auth.js";

const app = express();
app.use(cors());
app.use(express.json());

// '/' health check
app.get("/", (_, res) => res.send("server is running... 🚀"));

// Routes
app.use("/auth", authRoutes);

app.listen(PORT, () => {
  console.log(`app listening at http://localhost:${PORT}`);
});