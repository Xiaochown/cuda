# SETUP LAPTOP — environment buat ngembangin Cuda

Target: laptop Windows user (`zie`). **Wajib pakai WSL2** — Cuda Agent butuh shell Linux, git, Playwright, dan `bash`. Di PowerShell native, tool `shell`/`python` bakal bermasalah.

---

## A. Wajib: WSL2 + Ubuntu

Buka **PowerShell as Administrator**:

```powershell
wsl --install -d Ubuntu
# restart kalau diminta, lalu buka Ubuntu dari Start Menu, bikin username + password
```

Di dalam Ubuntu (WSL):

```bash
sudo apt update && sudo apt install -y build-essential git curl ripgrep ffmpeg \
  python3 python3-pip unzip
```

**Node 22** (jangan pakai Node bawaan apt — terlalu tua):

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v   # harus >= v22
npm i -g npm@latest
```

**GitHub CLI:**

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh
gh auth login    # pilih GitHub.com → HTTPS → login via browser/token (akun Xiaochown)
gh auth status
```

**Clone repo:**

```bash
cd ~ && git clone https://github.com/Xiaochown/cuda.git && cd cuda
```

> Tip: taruh project di filesystem WSL (`~/cuda`), **bukan** di `/mnt/c/...` — jauh lebih cepat dan tidak bikin masalah permission/symlink.

---

## B. Opsional tapi disarankan

**Playwright (tool browser Cuda Agent):**

```bash
npx playwright install --with-deps chromium
```

**pm2 (biar agent-node jalan terus):**

```bash
sudo npm i -g pm2
```

**Tailscale (biar HP user bisa akses app dari luar rumah):**

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip -4      # catat IP-nya, dipakai buat akses dari HP
```

**Akses folder Windows dari WSL** (kalau file ada di `C:\`): `cd /mnt/c/Users/zie/...`

---

## C. Env untuk Cuda

Bikin `.env` di root repo (**jangan di-commit** — sudah masuk `.gitignore`):

```bash
cat > .env <<'EOF'
# Provider untuk testing (BYOE — pakai key milik user)
TEST_PROVIDER_LABEL=TeamORouter
TEST_PROVIDER_BASE_URL=https://api.teamorouter.com/v1
TEST_PROVIDER_API_KEY=sk-xxxxx

# Secret untuk enkripsi kredensial user (AES-256-GCM) — generate:
#   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
CUDA_SECRET_KEY=isi-64-hex-char

# Agent node
AGENT_NODE_PORT=9400
AGENT_NODE_HMAC_SECRET=ganti-dengan-random-string
EOF
chmod 600 .env
```

**Minta user** kasih satu `base_url` + `api_key` OpenAI-compatible untuk testing (bisa dari provider apa pun yang dia punya).

---

## D. Jalankan

```bash
npm install                 # dari root (npm workspaces)
npm run dev                 # web  → http://localhost:3000
npm run dev:agent           # agent-node → http://localhost:9400
```

Kalau mau HP bisa akses (mis. buat uji mobile):

```bash
npm run dev -- --hostname 0.0.0.0
# lalu dari HP buka http://<tailscale-ip>:3000
```

---

## E. Verifikasi setup

```bash
node -v                 # >= v22
git -v
gh auth status          # logged in
npm -v                  # 10+
npx playwright --version
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:9400/health   # 200 setelah agent-node jalan
```

---

## F. Pitfall yang sudah diketahui (hemat waktu)

1. **Jangan install project di `/mnt/c/...`** — `npm install` lambat dan symlink rusak. Pakai `~/cuda`.
2. **Node < 22 bikin gagal build Next.js 16** — pakai NodeSource 22 seperti di atas.
3. **`npm audit fix --force` jangan dijalankan** — merusak dependency tree.
4. **Playwright di WSL butuh `--with-deps`** untuk library sistem (kalau tidak, Chromium gagal start).
5. **Port < 1024 butuh root** di WSL — pakai 3000 (web) dan 9400 (agent-node).
6. **Kalau `gh` belum login**, clone repo private akan gagal dengan "repository not found" (pesan menyesatkan — itu masalah auth, bukan repo hilang).
7. **Windows Firewall** bisa memblok akses dari HP ke port WSL — pakai Tailscale (cara paling gampang) atau tambahkan rule inbound.
8. **Deploy Vercel** butuh login sendiri: `npx vercel login` lalu `npx vercel --prod` dari `apps/web`. Repo GitHub sudah connect-able untuk auto-deploy.
