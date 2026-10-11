import static spark.Spark.*;
import com.google.gson.Gson;
import java.util.HashMap;
import java.util.Map;

public class BackendServer {
    public static void main(String[] args) {
        // Set port to match your frontend fetch URL
        port(5000);

        // Enable CORS so your HTML/JS frontend can talk to Java
        enableCORS();

        // Temporary memory storage (equivalent to Python's dictionary)
        Map<String, String> fakeDatabase = new HashMap<>();
        Gson gson = new Gson();

        // ---------- SIGNUP ENDPOINT ----------
        post("/api/signup", (req, res) => {
            res.type("application/json");
            
            // Parse incoming JSON body
            Map<String, String> body = gson.fromJson(req.body(), Map.class);
            String email = body.get("email");
            String password = body.get("password");

            Map<String, Object> responseMap = new HashMap<>();

            if (email == null || password == null || email.isEmpty() || password.isEmpty()) {
                res.status(400);
                responseMap.put("success", false);
                responseMap.put("message", "Email and password are required!");
                return gson.toJson(responseMap);
            }

            if (fakeDatabase.containsKey(email)) {
                res.status(400);
                responseMap.put("success", false);
                responseMap.put("message", "Account already exists!");
                return gson.toJson(responseMap);
            }

            // Save user to memory
            fakeDatabase.put(email, password);
            System.out.println("New user registered: " + email);

            res.status(200);
            responseMap.put("success", true);
            responseMap.put("message", "Signup successful!");
            return gson.toJson(responseMap);
        });

        // ---------- LOGIN ENDPOINT ----------
        post("/api/login", (req, res) => {
            res.type("application/json");
            
            Map<String, String> body = gson.fromJson(req.body(), Map.class);
            String email = body.get("email");
            String password = body.get("password");

            Map<String, Object> responseMap = new HashMap<>();

            if (fakeDatabase.containsKey(email) && fakeDatabase.get(email).equals(password)) {
                res.status(200);
                responseMap.put("success", true);
                responseMap.put("message", "Login successful!");
                return gson.toJson(responseMap);
            }

            res.status(401);
            responseMap.put("success", false);
            responseMap.put("message", "Invalid email or password!");
            return gson.toJson(responseMap);
        });
    }

    // Helper method to enable CORS headers in Spark Java
    private static void enableCORS() {
        options("/*", (request, response) -> {
            String accessControlRequestHeaders = request.headers("Access-Control-Request-Headers");
            if (accessControlRequestHeaders != null) {
                response.header("Access-Control-Allow-Headers", accessControlRequestHeaders);
            }
            String accessControlRequestMethod = request.headers("Access-Control-Request-Method");
            if (accessControlRequestMethod != null) {
                response.header("Access-Control-Allow-Methods", accessControlRequestMethod);
            }
            return "OK";
        });

        before((request, response) -> {
            response.header("Access-Control-Allow-Origin", "*");
            response.header("Access-Control-Allow-Request-Method", "GET,POST,PUT,DELETE,OPTIONS");
            response.header("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Requested-With");
        });
    }
}