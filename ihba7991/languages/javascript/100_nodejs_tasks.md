# 100 Node.js Tasks - Complete Mastery Path

## Week 1: Node.js Fundamentals (Tasks 1-30)

### Node.js Basics (1-10)
1. Install Node.js and verify installation (node -v, npm -v)
2. Create and run your first Node.js script with console.log
3. Understand the global object and process object
4. Use process.argv to read command-line arguments
5. Access environment variables using process.env
6. Create a package.json file using npm init
7. Install and use a package from npm (e.g., chalk for colored console)
8. Understand the difference between dependencies and devDependencies
9. Use require() to import built-in modules
10. Create and export your own module using module.exports

### Core Modules (11-22)
11. Use fs.readFile() to read a file asynchronously
12. Use fs.readFileSync() for synchronous file reading
13. Write data to a file using fs.writeFile()
14. Append data to a file using fs.appendFile()
15. Delete a file using fs.unlink()
16. Create a directory using fs.mkdir()
17. Read directory contents using fs.readdir()
18. Use path module to join and resolve paths
19. Work with __dirname and __filename
20. Use os module to get system information
21. Create a simple event emitter using events module
22. Handle streams with fs.createReadStream()

### Asynchronous Programming (23-30)
23. Understand callbacks with setTimeout and setInterval
24. Handle callback errors (error-first callbacks)
25. Convert callback-based function to Promise
26. Use Promise.then() and Promise.catch()
27. Chain multiple Promises
28. Use Promise.all() to handle multiple async operations
29. Use async/await syntax for cleaner async code
30. Handle errors with try-catch in async functions

## Week 2: HTTP, Express & REST APIs (Tasks 31-60)

### HTTP Module (31-38)
31. Create a basic HTTP server using http module
32. Handle different routes manually
33. Parse URL and query parameters
34. Handle POST requests and read body data
35. Set response headers and status codes
36. Serve static HTML files
37. Create a simple JSON API endpoint
38. Implement basic routing logic

### Express.js Fundamentals (39-52)
39. Install Express and create a basic server
40. Create multiple routes (GET, POST, PUT, DELETE)
41. Use route parameters (/users/:id)
42. Access query parameters (?name=value)
43. Parse JSON request body using express.json()
44. Serve static files using express.static()
45. Use express.Router() for modular routes
46. Create custom middleware function
47. Use third-party middleware (morgan for logging)
48. Handle errors with error-handling middleware
49. Chain multiple middleware functions
50. Use next() to pass control to next middleware
51. Implement CORS middleware
52. Add request validation middleware

### Building REST APIs (53-60)
53. Create a simple in-memory data store (array)
54. Implement GET /api/users (get all users)
55. Implement GET /api/users/:id (get single user)
56. Implement POST /api/users (create user)
57. Implement PUT /api/users/:id (update user)
58. Implement DELETE /api/users/:id (delete user)
59. Add input validation for POST/PUT requests
60. Return appropriate status codes (200, 201, 404, 400, 500)

## Week 3: Databases, Authentication & Advanced Topics (Tasks 61-85)

### Working with MongoDB (61-70)
61. Install MongoDB and mongoose
62. Connect to MongoDB database
63. Define a Mongoose schema and model
64. Create documents using model.create()
65. Find documents using model.find() and model.findById()
66. Update documents using model.findByIdAndUpdate()
67. Delete documents using model.findByIdAndDelete()
68. Add validation to Mongoose schemas
69. Use Mongoose middleware (pre/post hooks)
70. Implement pagination for large datasets

### Authentication & Security (71-80)
71. Hash passwords using bcrypt
72. Create user registration endpoint
73. Create user login endpoint
74. Generate JWT tokens
75. Verify JWT tokens in middleware
76. Protect routes with authentication middleware
77. Implement refresh tokens
78. Use environment variables for secrets (.env file)
79. Implement rate limiting
80. Add helmet for security headers

### File Uploads & Email (81-85)
81. Handle file uploads using multer
82. Validate file types and sizes
83. Store files locally and save path to database
84. Send emails using nodemailer
85. Create email templates

## Week 4: Testing, WebSockets & Deployment (Tasks 86-100)

### Testing (86-91)
86. Setup Jest for testing
87. Write unit tests for utility functions
88. Test Express routes using supertest
89. Mock database calls in tests
90. Test authentication middleware
91. Measure test coverage

### Real-time Features (92-95)
92. Setup Socket.io server
93. Handle client connections and disconnections
94. Emit and listen to events
95. Broadcast messages to all clients

### Advanced Topics (96-98)
96. Implement API versioning (/api/v1/, /api/v2/)
97. Add request logging and monitoring
98. Implement caching with Redis basics

### Deployment (99-100)
99. Prepare app for production (environment configs)
100. Deploy Node.js app (Heroku, Railway, or DigitalOcean)

---

## Learning Path Notes

**Prerequisites**:
- JavaScript fundamentals (ES6+)
- Basic understanding of HTTP
- Command line basics

**Required Tools**:
- Node.js (v18+ LTS recommended)
- npm or yarn
- Postman or Thunder Client for API testing
- MongoDB (local or Atlas)
- VS Code with Node.js extensions

**Time estimate**: 60-80 hours total

## Essential Node.js Concepts

### Core Concepts
- Event-driven, non-blocking I/O
- Single-threaded event loop
- Asynchronous programming patterns
- Module system (CommonJS and ES Modules)
- NPM ecosystem

### Important Modules

**Built-in**:
- fs (file system)
- http/https (web servers)
- path (file paths)
- os (operating system)
- events (event emitter)
- stream (data streaming)
- crypto (cryptography)

**Popular Packages**:
- express (web framework)
- mongoose (MongoDB ODM)
- dotenv (environment variables)
- jsonwebtoken (JWT auth)
- bcrypt (password hashing)
- nodemailer (emails)
- socket.io (real-time)
- jest (testing)

## Express.js Key Concepts

**Middleware Flow**:
```
Request → Middleware 1 → Middleware 2 → Route Handler → Response
```

**Middleware Types**:
- Application-level middleware
- Router-level middleware
- Error-handling middleware
- Built-in middleware (express.json, express.static)
- Third-party middleware

**REST API Best Practices**:
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Return appropriate status codes
- Use consistent URL naming (plural nouns)
- Version your API
- Implement proper error handling
- Add request validation
- Use pagination for large datasets

## Common Patterns

### Project Structure
```
project/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   ├── utils/
│   └── app.js
├── tests/
├── .env
├── .gitignore
└── package.json
```

### Error Handling
```javascript
// Async error wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Global error handler
app.use((err, req, res, next) => {
  res.status(err.statusCode || 500).json({
    success: false,
    message: err.message
  });
});
```

## Security Best Practices

1. **Input Validation**: Validate all user inputs
2. **Authentication**: Use JWT or sessions securely
3. **Password Storage**: Always hash passwords (bcrypt)
4. **Environment Variables**: Never commit secrets
5. **Rate Limiting**: Prevent abuse
6. **CORS**: Configure properly
7. **Helmet**: Add security headers
8. **SQL Injection**: Use parameterized queries
9. **XSS**: Sanitize user input
10. **HTTPS**: Use in production

## Database Choices

**SQL**:
- PostgreSQL (pg package)
- MySQL (mysql2 package)
- SQLite (better-sqlite3)

**NoSQL**:
- MongoDB (mongoose)
- Redis (redis package)

**ORMs/ODMs**:
- Sequelize (SQL ORM)
- TypeORM
- Prisma
- Mongoose (MongoDB ODM)

## Testing Strategy

**Test Types**:
- Unit tests (individual functions)
- Integration tests (API endpoints)
- End-to-end tests (full user flows)

**Tools**:
- Jest (test runner)
- Supertest (HTTP assertions)
- Sinon (mocking)
- Chai (assertions)

## Performance Tips

1. Use async/await properly
2. Implement caching (Redis)
3. Use connection pooling for databases
4. Enable gzip compression
5. Use CDN for static assets
6. Implement pagination
7. Use indexes in databases
8. Profile with Node.js profiler
9. Use clustering for multi-core
10. Monitor with PM2 or similar

## Common Mistakes to Avoid

- Blocking the event loop
- Not handling errors properly
- Callback hell (use async/await)
- Not validating user input
- Storing secrets in code
- Not using environment variables
- Synchronous operations in production
- Not implementing logging
- Missing error handling in async code
- Not using a process manager in production

## Next Steps After Completion

1. **TypeScript**: Add type safety to Node.js
2. **GraphQL**: Learn Apollo Server
3. **Microservices**: Service architecture patterns
4. **Message Queues**: RabbitMQ, Bull
5. **Docker**: Containerization
6. **CI/CD**: Automated deployment
7. **WebSockets**: Advanced real-time features
8. **Serverless**: AWS Lambda, Vercel Functions
9. **Testing**: Advanced testing strategies
10. **Performance**: Advanced optimization

## Project Ideas

- RESTful blog API with authentication
- Real-time chat application
- Task management API
- E-commerce backend
- Social media API
- File upload service
- URL shortener
- Email newsletter service
- Weather API aggregator
- Authentication service (OAuth)
