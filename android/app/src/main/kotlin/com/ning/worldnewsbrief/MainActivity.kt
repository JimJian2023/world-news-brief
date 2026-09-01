package com.ning.worldnewsbrief

import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.Uri
import android.os.Bundle
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            WorldNewsApp()
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WorldNewsApp() {
    val context = LocalContext.current
    val url = "https://jimjian2023.github.io/world-news-brief/"

    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFF6366F1),    // Indigo
            onPrimary = Color.White,
            surface = Color(0xFF0F172A),     // Slate dark
            onSurface = Color(0xFFE2E8F0),
            background = Color(0xFF020617),
        )
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("\uD83C\uDF0D World News Brief", style = MaterialTheme.typography.titleMedium) },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color(0xFF1E1B4B),
                        titleContentColor = Color.White
                    ),
                    actions = {
                        IconButton(onClick = {
                            // Refresh by reloading
                            val wv = context.getSharedPreferences("app", Context.MODE_PRIVATE)
                                .getString("webview_instance", null)
                        }) {
                            Icon(Icons.Default.Refresh, contentDescription = "Refresh")
                        }
                    }
                )
            },
            bottomBar = {
                BottomAppBar(
                    containerColor = Color(0xFF1E1B4B)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        TextButton(onClick = {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://jimjian2023.github.io/world-news-brief/"))
                            context.startActivity(intent)
                        }) {
                            Text("\uD83C\uDF10 Open in Browser", color = Color.White, style = MaterialTheme.typography.labelSmall)
                        }
                        TextButton(onClick = {
                            Toast.makeText(context, "News updated twice daily", Toast.LENGTH_SHORT).show()
                        }) {
                            Text("\u23F0 9 AM & 5 PM", color = Color.White, style = MaterialTheme.typography.labelSmall)
                        }
                    }
                }
            }
        ) { paddingValues ->
            Box(modifier = Modifier.padding(paddingValues)) {
                if (isOnline(context)) {
                    NewsWebView(url = url)
                } else {
                    OfflineMessage()
                }
            }
        }
    }
}

@Composable
fun NewsWebView(url: String) {
    AndroidView(
        factory = { ctx ->
            WebView(ctx).apply {
                settings.apply {
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    loadWithOverviewMode = true
                    useWideViewPort = true
                    builtInZoomControls = true
                    displayZoomControls = false
                    setSupportZoom(true)
                    mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                    userAgentString = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 WorldNewsBrief-App"
                    cacheMode = android.webkit.WebSettings.LOAD_DEFAULT
                }

                webViewClient = object : WebViewClient() {
                    override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                        // Open external links in browser
                        val reqUrl = request?.url?.toString() ?: return false
                        if (reqUrl.contains("github.io/world-news-brief") ||
                            reqUrl.startsWith("javascript:") ||
                            reqUrl.startsWith("about:")) {
                            return false // Load in WebView
                        }
                        // External links open in browser
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(reqUrl))
                        ctx.startActivity(intent)
                        return true
                    }

                    override fun onReceivedError(
                        view: WebView?,
                        errorCode: Int,
                        description: String?,
                        failingUrl: String?
                    ) {
                        Toast.makeText(ctx, "Network error. Pull down to retry.", Toast.LENGTH_LONG).show()
                    }
                }

                loadUrl(url)
            }
        },
        modifier = Modifier.fillMaxSize()
    )
}

@Composable
fun OfflineMessage() {
    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center
        ) {
            Text("\uD83D\uDCF5 No internet connection",
                style = MaterialTheme.typography.headlineSmall,
                modifier = Modifier.padding(16.dp))
            Text("Please check your network and try again.",
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.padding(horizontal = 16.dp))
        }
    }
}

fun isOnline(context: Context): Boolean {
    val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    val network = cm.activeNetwork ?: return false
    val capabilities = cm.getNetworkCapabilities(network) ?: return false
    return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
}
