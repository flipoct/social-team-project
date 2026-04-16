import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

async function ensureTable() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS comments (
      id BIGSERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      message TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
  `);
}

function json(res, status, data) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(JSON.stringify(data));
}

export default async function handler(req, res) {
  try {
    await ensureTable();

    if (req.method === "GET") {
      const result = await pool.query(`
        SELECT id, name, message, created_at
        FROM comments
        ORDER BY created_at DESC
        LIMIT 100
      `);

      return json(res, 200, {
        comments: result.rows.map((row) => ({
          id: String(row.id),
          name: row.name,
          message: row.message,
          createdAt: row.created_at
        }))
      });
    }

    if (req.method === "POST") {
      let body = "";

      await new Promise((resolve, reject) => {
        req.on("data", (chunk) => {
          body += chunk;
        });
        req.on("end", resolve);
        req.on("error", reject);
      });

      const parsed = JSON.parse(body || "{}");
      const name = String(parsed.name || "").trim();
      const message = String(parsed.message || "").trim();

      if (!name || !message) {
        return json(res, 400, { error: "이름과 내용을 모두 입력해 주세요." });
      }

      const result = await pool.query(
        `INSERT INTO comments (name, message)
         VALUES ($1, $2)
         RETURNING id, name, message, created_at`,
        [name, message]
      );

      const row = result.rows[0];

      return json(res, 201, {
        comment: {
          id: String(row.id),
          name: row.name,
          message: row.message,
          createdAt: row.created_at
        }
      });
    }

    if (req.method === "DELETE") {
      const id = req.url?.split("?id=")[1];

      if (!id) {
        return json(res, 400, { error: "id가 필요합니다." });
      }

      await pool.query(`DELETE FROM comments WHERE id = $1`, [id]);
      return json(res, 200, { ok: true });
    }

    return json(res, 405, { error: "허용되지 않은 메서드입니다." });
  } catch (error) {
    console.error(error);
    return json(res, 500, { error: "서버 오류가 발생했습니다." });
  }
}