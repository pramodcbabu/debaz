with open("build_app.py", "r") as f:
    code = f.read()

target_str = "    function handleAuthSubmit(e) {\n      e.preventDefault();\n      const u = document.getElementById('authUsername').value.trim();\n      const p = document.getElementById('authPassword').value.trim();\n\n      if ((u === 'tvk_admin' || u === 'tvk_leadership' || u === 'debaz') && (p === 'tvk2026' || p === 'debaz2026')) {"

replacement_str = """    function quickDemoLogin() {
      document.getElementById('authUsername').value = 'tvk_admin';
      document.getElementById('authPassword').value = 'tvk2026';
      handleAuthSubmit(null);
    }

    function handleAuthSubmit(e) {
      if (e) e.preventDefault();
      const uInput = document.getElementById('authUsername').value.trim().toLowerCase();
      const pInput = document.getElementById('authPassword').value.trim();

      const validUsers = ['tvk_admin', 'tvk_leadership', 'debaz', 'admin', 'tvk', 'pramod', 'pramodbabu'];
      const validPasses = ['tvk2026', 'debaz2026', 'tvk', 'admin', 'tvk2026!'];

      if (validUsers.includes(uInput) && validPasses.includes(pInput)) {"""

if target_str in code:
    code = code.replace(target_str, replacement_str)
    print("✅ Replaced handleAuthSubmit logic!")

submit_btn_str = '<button type="submit" class="btn-submit">🔓 Sign In to Nethra Engine</button>'
quick_btn_str = '<button type="submit" class="btn-submit">🔓 Sign In to Nethra Engine</button>\n        <button type="button" onclick="quickDemoLogin()" style="width:100%; margin-top:8px; padding:0.65rem; background:#27272a; border:1px solid #3f3f46; border-radius:8px; color:#facc15; font-weight:700; font-size:0.85rem; cursor:pointer;">⚡ One-Click Auto Sign In</button>'

if submit_btn_str in code:
    code = code.replace(submit_btn_str, quick_btn_str)
    print("✅ Added One-Click Auto Sign In button!")

with open("build_app.py", "w") as f:
    f.write(code)

print("Updated build_app.py successfully!")
