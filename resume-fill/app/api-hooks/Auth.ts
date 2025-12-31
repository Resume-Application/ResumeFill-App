export async function authUser(username: string, password: string) {
  try {
    const response = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username,
        password,
      }),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json();

    localStorage.setItem("access_token", data.access_token);

    return data;
    
  } catch (error) {
    console.error(error);
    return null;
  }
}


export async function signupUser(username: string, password: string) {
  try {
    const response = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Signup failed");
    }

    const data = await response.json();

    // Optionally, you could login the user immediately after signup
    // localStorage.setItem("access_token", data.access_token);

    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
}