import express from "express";

const router = express.Router();

router.get("/", (_, res) => res.send("auth server is running... 🐱‍🚀"));

export default router;