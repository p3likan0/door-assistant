mkdir -p certificates
echo "Generating certificates"
openssl req  -nodes -new -x509  -keyout certificates/key.pem -out certificates/cert.pem
echo "Uploading certificates to fs"
mos put certificates/cert.pem
mos put certificates/key.pem
echo "Configuring SSL"
mos config-set http.listen_addr=443 http.ssl_key=key.pem http.ssl_cert=cert.pem
