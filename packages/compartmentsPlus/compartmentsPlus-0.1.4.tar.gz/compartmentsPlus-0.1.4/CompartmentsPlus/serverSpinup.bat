start cmd.exe /K "python -m streamlit run CompartmentsPlusWeb.py  --server.headless=true"

%SystemRoot%\System32\timeout.exe 5

"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk http://localhost:8501 --edge-kiosk-type=fullscreen --no-first-run --force-dark-mode
