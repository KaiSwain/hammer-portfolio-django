// API Proxy to Backend Service
export async function GET(request) {
  return handleApiProxy(request, 'GET');
}

export async function POST(request) {
  return handleApiProxy(request, 'POST');
}

export async function PUT(request) {
  return handleApiProxy(request, 'PUT');
}

export async function DELETE(request) {
  return handleApiProxy(request, 'DELETE');
}

export async function PATCH(request) {
  return handleApiProxy(request, 'PATCH');
}

async function handleApiProxy(request, method) {
  const { pathname, search } = new URL(request.url);
  const apiPath = pathname.replace('/api/', '');
  
  // Backend service URL (internal DigitalOcean service communication)
  const backendUrl = process.env.BACKEND_INTERNAL_URL || 'http://hammer-backend:8000';
  const targetUrl = `${backendUrl}/api/${apiPath}${search}`;
  
  try {
    const headers = new Headers();
    
    // Copy relevant headers
    for (const [key, value] of request.headers.entries()) {
      if (key.toLowerCase() !== 'host' && key.toLowerCase() !== 'connection') {
        headers.set(key, value);
      }
    }
    
    const options = {
      method,
      headers,
    };
    
    // Add body for non-GET requests
    if (method !== 'GET' && method !== 'HEAD') {
      options.body = await request.arrayBuffer();
    }
    
    const response = await fetch(targetUrl, options);
    
    // Copy response headers
    const responseHeaders = new Headers();
    for (const [key, value] of response.headers.entries()) {
      responseHeaders.set(key, value);
    }
    
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders,
    });
    
  } catch (error) {
    console.error('API Proxy Error:', error);
    return Response.json(
      { error: 'Internal Server Error', details: error.message }, 
      { status: 500 }
    );
  }
}
