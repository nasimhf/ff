#!/bin/bash
mkdir -p $PREFIX/share/tempmail
cp tempmail.cpython-*.so $PREFIX/share/tempmail/
cp start.py $PREFIX/share/tempmail/

cat > $PREFIX/bin/tempmail << 'EOF'
#!/bin/bash
cd /data/data/com.termux/files/usr/share/tempmail
python3 start.py
EOF

chmod +x $PREFIX/bin/tempmail
chmod +x $PREFIX/share/tempmail/start.py
echo "✅ Installed! Run: tempmail"
