---
title: Java连接WebSocket服务忽略证书校验
layout: info
commentable: true
date: 2023-09-28
mathjax: true
mermaid: true
tags: [Blog]
categories: Blog
description: 
---

依赖

```xml
<dependency>
    <groupId>org.java-websocket</groupId>
    <artifactId>Java-WebSocket</artifactId>
    <version>1.5.2</version>
</dependency>
```

代码

```java
@Test
public void testWssWithWebSocketServer() throws Exception {
    TrustManager trustManager = new X509ExtendedTrustManager() {
        @Override
        public void checkClientTrusted(X509Certificate[] chain, String authType, Socket socket) throws CertificateException {

        }

        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType, Socket socket) throws CertificateException {

        }

        @Override
        public void checkClientTrusted(X509Certificate[] chain, String authType, SSLEngine engine) throws CertificateException {

        }

        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType, SSLEngine engine) throws CertificateException {

        }

        @Override
        public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException {

        }

        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {

        }

        @Override
        public X509Certificate[] getAcceptedIssuers() {
            return new X509Certificate[]{};
        }
    };
    SSLContext sslContext = SSLContext.getInstance("TLS");
    sslContext.init(null, new TrustManager[]{trustManager}, null);

    URI uri = URI.create("wss://127.0.0.1:8443/websocket");
    SSLSocketFactory socketFactory = sslContext.getSocketFactory();
    WebSocketClient webSocketClient = new WebSocketClient(uri) {
        @Override
        public void onOpen(ServerHandshake serverHandshake) {
            logger.info("onOpen");
        }

        @Override
        public void onMessage(String s) {
            logger.info("onMessage: " + s);
        }

        @Override
        public void onClose(int i, String s, boolean b) {
            logger.info("onClose");
        }

        @Override
        public void onError(Exception e) {
            logger.info("onError: " + e.getMessage(), e);
        }
    };
    webSocketClient.setSocketFactory(socketFactory);
    webSocketClient.connectBlocking();
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
    webSocketClient.send(simpleDateFormat.format(new Date()));
    webSocketClient.closeBlocking();
}
```



main.bundle.js:20686 Mixed Content: The page at '`https://***`' was loaded over HTTPS, but attempted to connect to the insecure WebSocket endpoint '`ws://***/websocket/***`'. This request has been blocked; this endpoint must be available over WSS.
Uncaught (in promise) DOMException: Failed to construct 'WebSocket': An insecure WebSocket connection may not be initiated from a page loaded over HTTPS.

https://blog.csdn.net/u012977315/article/details/84944708
