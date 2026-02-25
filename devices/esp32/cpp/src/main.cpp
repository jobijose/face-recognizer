#include <WiFi.h>
#include <HTTPClient.h>
#include <esp_camera.h>
#include "config.h"

#define CAPTURE_INTERVAL_MS 2000

// ---- Camera pins (XIAO ESP32-S3 Sense) ----
#define PWDN_GPIO_NUM  -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  10
#define SIOD_GPIO_NUM  40
#define SIOC_GPIO_NUM  39
#define Y9_GPIO_NUM    48
#define Y8_GPIO_NUM    11
#define Y7_GPIO_NUM    12
#define Y6_GPIO_NUM    14
#define Y5_GPIO_NUM    16
#define Y4_GPIO_NUM    18
#define Y3_GPIO_NUM    17
#define Y2_GPIO_NUM    15
#define VSYNC_GPIO_NUM 38
#define HREF_GPIO_NUM  47
#define PCLK_GPIO_NUM  13

void initCamera() {
    camera_config_t config = {};
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer   = LEDC_TIMER_0;
    config.pin_d0       = Y2_GPIO_NUM;
    config.pin_d1       = Y3_GPIO_NUM;
    config.pin_d2       = Y4_GPIO_NUM;
    config.pin_d3       = Y5_GPIO_NUM;
    config.pin_d4       = Y6_GPIO_NUM;
    config.pin_d5       = Y7_GPIO_NUM;
    config.pin_d6       = Y8_GPIO_NUM;
    config.pin_d7       = Y9_GPIO_NUM;
    config.pin_xclk     = XCLK_GPIO_NUM;
    config.pin_pclk     = PCLK_GPIO_NUM;
    config.pin_vsync    = VSYNC_GPIO_NUM;
    config.pin_href     = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn     = PWDN_GPIO_NUM;
    config.pin_reset    = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size   = FRAMESIZE_XGA;
    config.jpeg_quality = 8;
    config.fb_count     = 2;

    if (esp_camera_init(&config) != ESP_OK) {
        Serial.println("Camera init failed");
    }
}

void captureAndSend() {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Capture failed");
        return;
    }

    const String boundary = "----BoundaryXYZ123";
    const String contentType = "multipart/form-data; boundary=" + boundary;

    // Build multipart header and footer
    String head = "--" + boundary + "\r\n"
                  "Content-Disposition: form-data; name=\"image\"; filename=\"img.jpg\"\r\n"
                  "Content-Type: image/jpeg\r\n\r\n";
    String tail = "\r\n--" + boundary + "--\r\n";

    // Combine into a single buffer
    size_t totalLen = head.length() + fb->len + tail.length();
    uint8_t *body = (uint8_t *)malloc(totalLen);
    if (!body) {
        Serial.println("Memory error");
        esp_camera_fb_return(fb);
        return;
    }
    memcpy(body, head.c_str(), head.length());
    memcpy(body + head.length(), fb->buf, fb->len);
    memcpy(body + head.length() + fb->len, tail.c_str(), tail.length());

    esp_camera_fb_return(fb);

    HTTPClient http;
    http.begin(API_ENDPOINT);
    http.addHeader("Content-Type", contentType);
    int code = http.POST(body, totalLen);
    Serial.printf("HTTP %d\n", code);
    http.end();

    free(body);
}

void setup() {
    Serial.begin(115200);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println(" connected");

    initCamera();
}

void loop() {
    captureAndSend();
    delay(CAPTURE_INTERVAL_MS);
}