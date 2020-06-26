mkdir -p ~ / .streamlit /
eco "\
[geral] \ n \
email = \" seu betanialinux@gmail.com \ "\ n \
"> ~ / .streamlit / credentials.toml
echo “\
[servidor] \ n \
headless = true \ n \
enableCORS = false \ n \
port = $ PORT \ n \
“> ~ / .streamlit / config.toml
