# 100 React.js Tasks - Complete Mastery Path

## Week 1: React Fundamentals (Tasks 1-30)

### Setup & JSX Basics (1-8)
1. Create a React app using Create React App (npx create-react-app)
2. Understand the project structure (src, public, package.json)
3. Create your first functional component
4. Write JSX with embedded JavaScript expressions {}
5. Render a list of items using map()
6. Add conditional rendering using && and ternary operators
7. Apply inline styles to JSX elements
8. Import and use CSS files in components

### Components & Props (9-18)
9. Create a reusable Button component
10. Pass props to a component
11. Destructure props in function parameters
12. Set default props using defaultProps
13. Pass children props to components
14. Create a Card component that wraps content
15. Build a UserProfile component with multiple props
16. Create a component that renders different content based on props
17. Pass functions as props (callback props)
18. Build a ProductCard with image, title, price props

### State Management with useState (19-30)
19. Create a counter using useState
20. Build a toggle button (show/hide content)
21. Create a form with controlled input using useState
22. Build a todo list with add functionality
23. Implement delete functionality for todo items
24. Create a shopping cart with add/remove items
25. Build a multi-step form with state
26. Create a color picker that updates background
27. Implement a search filter for a list
28. Build a character counter for textarea
29. Create a simple calculator with state
30. Build a tab component with active state

## Week 2: Hooks & Side Effects (Tasks 31-55)

### useEffect Hook (31-40)
31. Fetch data from an API using useEffect
32. Update document title based on state
33. Create a timer/counter that runs on mount
34. Clean up side effects (clear interval on unmount)
35. Use dependency array to control when effect runs
36. Fetch data based on user input (search feature)
37. Create an infinite scroll implementation
38. Build a debounced search input
39. Implement localStorage persistence with useEffect
40. Create a component that fetches data on prop change

### Custom Hooks (41-48)
41. Create a useLocalStorage custom hook
42. Build a useWindowSize hook to track viewport dimensions
43. Create a useFetch hook for API calls
44. Implement a useToggle hook
45. Build a useDebounce hook
46. Create a useOnClickOutside hook
47. Implement a usePrevious hook to track previous state
48. Build a useKeyPress hook for keyboard events

### useContext & Context API (49-55)
49. Create a Context for theme (light/dark mode)
50. Use useContext to consume theme context
51. Build a global state for user authentication
52. Create a context for language/localization
53. Implement a shopping cart context
54. Build a notification/toast context
55. Create nested contexts for complex state

## Week 3: Advanced Patterns & Routing (Tasks 56-80)

### useReducer & Complex State (56-62)
56. Create a counter using useReducer
57. Build a todo app with useReducer
58. Implement a shopping cart with useReducer
59. Create a form with complex validation using useReducer
60. Build a game state manager (tic-tac-toe) with useReducer
61. Combine useReducer with useContext for global state
62. Implement undo/redo functionality with useReducer

### React Router (63-72)
63. Install and setup React Router
64. Create basic routes (Home, About, Contact)
65. Use Link component for navigation
66. Implement dynamic routes with URL parameters
67. Access URL parameters using useParams
68. Use useNavigate for programmatic navigation
69. Create a 404 Not Found page
70. Implement nested routes
71. Use useLocation to access current location
72. Add route guards/protected routes

### Forms & Validation (73-80)
73. Create a basic form with validation
74. Build a registration form with multiple inputs
75. Implement form validation with error messages
76. Use a library like Formik for form management
77. Add validation with Yup schema
78. Create a multi-step form with validation
79. Build a file upload component
80. Implement form submission with loading state

## Week 4: Performance, Testing & Production (Tasks 81-100)

### Performance Optimization (81-88)
81. Use React.memo to prevent unnecessary re-renders
82. Implement useCallback to memoize functions
83. Use useMemo to memoize expensive calculations
84. Implement lazy loading with React.lazy and Suspense
85. Create a virtualized list for large datasets
86. Optimize images with lazy loading
87. Use code splitting for better performance
88. Implement error boundaries for error handling

### Advanced Patterns (89-94)
89. Create a Higher Order Component (HOC)
90. Implement render props pattern
91. Build a compound component pattern
92. Create a controlled vs uncontrolled component example
93. Implement the Provider pattern
94. Use portals to render outside parent DOM

### Testing (95-97)
95. Write unit tests using React Testing Library
96. Test user interactions (clicks, input changes)
97. Test async operations and API calls

### Final Projects (98-100)
98. Build a weather app with API integration
99. Create a movie search app with TMDB API
100. Build a full-stack todo app with backend API

---

## Learning Path Notes

**Prerequisites**: 
- JavaScript fundamentals (ES6+)
- HTML & CSS basics
- Node.js and npm installed

**Recommended Tools**:
- VS Code with ES7+ React snippets
- React Developer Tools (browser extension)
- Create React App or Vite

**Time estimate**: 60-80 hours total

## Essential Concepts to Master

### Core Concepts
- JSX and component composition
- Props and state management
- Lifecycle through hooks
- Event handling
- Conditional rendering

### Advanced Concepts
- Context API for state management
- Custom hooks for reusability
- Performance optimization techniques
- Code splitting and lazy loading
- Error boundaries

## Common React Patterns

**Component Patterns**:
- Container/Presentational components
- Compound components
- Controlled components
- Higher-Order Components

**State Management**:
- useState for local state
- useReducer for complex state
- Context for global state
- (Later: Redux, Zustand, Recoil)

## React Ecosystem Libraries

**Must-Know**:
- React Router (routing)
- React Query or SWR (data fetching)
- Axios (HTTP requests)
- React Hook Form or Formik (forms)

**UI Libraries**:
- Material-UI (MUI)
- Chakra UI
- Ant Design
- Tailwind CSS

**State Management** (After basics):
- Redux Toolkit
- Zustand
- Jotai
- Recoil

## Best Practices

1. **Component Structure**: Keep components small and focused
2. **Props**: Use TypeScript or PropTypes for type safety
3. **State**: Lift state up only when needed
4. **Effects**: Keep useEffect dependencies accurate
5. **Performance**: Profile before optimizing
6. **Testing**: Test user behavior, not implementation

## Common Mistakes to Avoid

- Modifying state directly
- Missing dependency arrays in useEffect
- Over-using useEffect
- Prop drilling (use Context when needed)
- Premature optimization
- Not cleaning up side effects

## Next Steps After Completion

1. **TypeScript**: Add type safety to React
2. **Next.js**: Server-side rendering and routing
3. **State Management**: Redux Toolkit or Zustand
4. **Testing**: Deep dive into React Testing Library
5. **Animation**: Framer Motion or React Spring
6. **Mobile**: React Native

## Project Ideas for Practice

- E-commerce product catalog
- Social media dashboard
- Real-time chat application
- Task management system
- Recipe finder app
- Expense tracker
- Weather dashboard
- Movie/TV show database browser
