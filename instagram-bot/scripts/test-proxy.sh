#!/bin/bash

# Test proxy connectivity

echo "🔍 Testing proxy configuration..."

# Function to test proxy
test_proxy() {
    local proxy_url=$1
    local proxy_name=$2
    
    echo -n "Testing $proxy_name... "
    
    # Test with curl
    response=$(curl -x "$proxy_url" -s -o /dev/null -w "%{http_code}" --connect-timeout 10 http://httpbin.org/ip)
    
    if [ "$response" = "200" ]; then
        echo "✅ Working"
        # Get IP address
        ip=$(curl -x "$proxy_url" -s --connect-timeout 10 http://httpbin.org/ip | grep -oP '"origin": "\K[^"]+')
        echo "  IP: $ip"
    else
        echo "❌ Failed (HTTP $response)"
    fi
}

# Test proxies from environment variables
if [ ! -z "$PROXY_HOST" ]; then
    proxy_url="$PROXY_HOST:$PROXY_PORT"
    if [ ! -z "$PROXY_USERNAME" ]; then
        proxy_url="$PROXY_USERNAME:$PROXY_PASSWORD@$proxy_url"
    fi
    test_proxy "$proxy_url" "Default Proxy"
fi

# Test multiple bot proxies if configured
for i in 1 2 3; do
    host_var="BOT${i}_PROXY_HOST"
    port_var="BOT${i}_PROXY_PORT"
    user_var="BOT${i}_PROXY_USERNAME"
    pass_var="BOT${i}_PROXY_PASSWORD"
    
    if [ ! -z "${!host_var}" ]; then
        proxy_url="${!host_var}:${!port_var}"
        if [ ! -z "${!user_var}" ]; then
            proxy_url="${!user_var}:${!pass_var}@$proxy_url"
        fi
        test_proxy "$proxy_url" "Bot $i Proxy"
    fi
done

echo ""
echo "Proxy test complete!"