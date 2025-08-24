# Homlo Web - Frontend

Next.js 14 frontend application for the Homlo platform - Pakistan's premier Airbnb-style marketplace.

## 🚀 Features

- **Next.js 14**: Latest React framework with App Router
- **TypeScript**: Full type safety and better developer experience
- **Tailwind CSS**: Utility-first CSS framework with custom design system
- **shadcn/ui**: High-quality, accessible UI components
- **Framer Motion**: Smooth animations and transitions
- **React Query**: Server state management and caching
- **Zustand**: Lightweight client state management
- **Next-intl**: Internationalization (English/Urdu)
- **Leaflet Maps**: Interactive maps with OpenStreetMap
- **Real-time Chat**: WebSocket-based messaging
- **PWA Ready**: Progressive Web App capabilities
- **Responsive Design**: Mobile-first approach

## 🏗️ Architecture

```
src/
├── app/                 # Next.js App Router pages
├── components/          # Reusable UI components
│   ├── ui/             # shadcn/ui components
│   ├── forms/          # Form components
│   ├── layout/         # Layout components
│   └── features/       # Feature-specific components
├── hooks/              # Custom React hooks
├── lib/                # Utility libraries
├── types/              # TypeScript type definitions
├── utils/              # Helper functions
├── styles/             # Global styles and Tailwind config
└── context/            # React Context providers
```

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.3
- **Styling**: Tailwind CSS 3.3
- **UI Components**: shadcn/ui + Radix UI
- **State Management**: Zustand + React Query
- **Maps**: Leaflet + OpenStreetMap
- **Forms**: React Hook Form + Zod
- **Testing**: Jest + Testing Library + Playwright
- **Code Quality**: ESLint + Prettier + Husky

## 📋 Prerequisites

- Node.js 20+
- npm or yarn
- Modern web browser with ES2020 support

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd homlo/apps/web
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Environment Configuration

```bash
cp env.example .env.local
# Edit .env.local with your configuration
```

### 4. Start Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🌍 Environment Variables

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# MinIO Configuration
NEXT_PUBLIC_MINIO_ENDPOINT=http://localhost:9000
NEXT_PUBLIC_MINIO_BUCKET=homlo-assets

# Application Configuration
NEXT_PUBLIC_APP_NAME=Homlo
NEXT_PUBLIC_APP_VERSION=1.0.0

# Feature Flags
NEXT_PUBLIC_ENABLE_WHATSAPP_SHARE=true
NEXT_PUBLIC_ENABLE_CASH_ON_ARRIVAL=true
NEXT_PUBLIC_ENABLE_GUEST_SCORING=true

# Maps (Optional)
NEXT_PUBLIC_MAPBOX_TOKEN=
NEXT_PUBLIC_MAPTILER_TOKEN=
```

## 🎨 Design System

### Color Palette

```css
/* Primary Colors - Pakistan Theme */
--primary-50: #f0fdf4;
--primary-500: #22c55e;  /* Main Green */
--primary-900: #14532d;

/* Secondary Colors */
--secondary-500: #eab308;  /* Gold Accent */
--accent-500: #ec4899;     /* Pink Accent */

/* Pakistan-specific Colors */
--pakistan-green: #01411C;
--pakistan-white: #FFFFFF;
```

### Typography

- **English**: Inter (system font fallback)
- **Urdu**: Noto Nastaliq Urdu
- **Headings**: Bold weights for hierarchy
- **Body**: Regular weight for readability

### Component Variants

All components follow consistent variant patterns:

```tsx
// Button variants
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>

// Size variants
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
```

## 🗺️ Key Pages

### Public Pages

- **Homepage**: Featured listings, search, city collections
- **Search Results**: Filtered listings with map and list views
- **Listing Details**: Property information, photos, booking
- **User Profiles**: Host and guest profiles with reviews
- **About/Help**: Platform information and support

### Authenticated Pages

- **Dashboard**: User overview and quick actions
- **Host Dashboard**: Listing management, bookings, analytics
- **Guest Dashboard**: Trips, saved listings, reviews
- **Inbox**: Chat conversations with hosts/guests
- **Settings**: Profile, preferences, security

### Admin Pages

- **Admin Dashboard**: Platform overview and metrics
- **User Management**: User moderation and verification
- **Content Moderation**: Listing and review approval
- **System Health**: Service monitoring and alerts

## 🧩 Core Components

### Layout Components

```tsx
// Main layout wrapper
<Layout>
  <Header />
  <main>{children}</main>
  <Footer />
</Layout>

// Page-specific layouts
<HostLayout>
  <HostSidebar />
  {children}
</HostLayout>
```

### Form Components

```tsx
// Form with validation
<Form {...form}>
  <FormField
    control={form.control}
    name="email"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input {...field} type="email" />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
</Form>
```

### Data Display

```tsx
// Listing cards
<ListingCard
  listing={listing}
  onFavorite={handleFavorite}
  onBook={handleBook}
/>

// Search filters
<SearchFilters
  filters={filters}
  onFilterChange={handleFilterChange}
/>
```

## 🌐 Internationalization

### Language Support

- **English**: Default language (LTR)
- **Urdu**: Full RTL support with proper fonts

### Implementation

```tsx
// Language switching
const { locale, setLocale } = useLocale();

// Translation usage
const t = useTranslations('common');
return <h1>{t('welcome')}</h1>;

// RTL support
<div dir={locale === 'ur' ? 'rtl' : 'ltr'}>
  {content}
</div>
```

### Translation Files

```json
// en.json
{
  "common": {
    "welcome": "Welcome to Homlo",
    "search": "Search properties"
  }
}

// ur.json
{
  "common": {
    "welcome": "ہوملو میں خوش آمدید",
    "search": "پراپرٹیز تلاش کریں"
  }
}
```

## 🗺️ Maps Integration

### Leaflet Implementation

```tsx
// Map component
<MapContainer center={[24.8607, 67.0011]} zoom={10}>
  <TileLayer
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  />
  {listings.map(listing => (
    <Marker
      key={listing.id}
      position={[listing.latitude, listing.longitude]}
    >
      <Popup>
        <ListingPopup listing={listing} />
      </Popup>
    </Marker>
  ))}
</MapContainer>
```

### Features

- **Interactive Markers**: Click for listing details
- **Cluster Markers**: Group nearby listings
- **Search by Map**: Draw areas to search
- **Location Picker**: Select coordinates for listings

## 💬 Real-time Features

### WebSocket Integration

```tsx
// Chat hook
const { messages, sendMessage, isConnected } = useChat(threadId);

// Send message
const handleSend = (text: string) => {
  sendMessage({
    text,
    timestamp: new Date(),
    senderId: currentUser.id
  });
};
```

### Features

- **Real-time Messaging**: Instant message delivery
- **Typing Indicators**: Show when user is typing
- **Online Status**: User availability indicators
- **Read Receipts**: Message read confirmation

## 📱 Progressive Web App

### PWA Features

- **Offline Support**: Service worker caching
- **Install Prompt**: Add to home screen
- **Push Notifications**: Booking and chat alerts
- **Background Sync**: Offline data synchronization

### Configuration

```json
// manifest.json
{
  "name": "Homlo - Pakistan's Premier Rental Platform",
  "short_name": "Homlo",
  "description": "Find and book amazing properties across Pakistan",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#22c55e",
  "background_color": "#ffffff"
}
```

## 🧪 Testing

### Test Structure

```bash
tests/
├── unit/              # Component unit tests
├── integration/       # Feature integration tests
├── e2e/              # End-to-end tests
└── fixtures/          # Test data
```

### Running Tests

```bash
# Unit tests
npm test

# E2E tests
npm run e2e

# Test coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Testing Utilities

```tsx
// Component testing
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('renders login form', () => {
  render(<LoginForm />);
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
});

test('submits form with valid data', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);
  
  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.click(screen.getByRole('button', { name: /login/i }));
  
  expect(mockSubmit).toHaveBeenCalledWith({
    email: 'test@example.com'
  });
});
```

## 🚀 Performance Optimization

### Next.js Features

- **Image Optimization**: Automatic WebP conversion
- **Code Splitting**: Automatic route-based splitting
- **Static Generation**: Pre-rendered pages where possible
- **Incremental Static Regeneration**: Fresh content updates

### React Optimizations

- **Memoization**: React.memo for expensive components
- **Lazy Loading**: Dynamic imports for heavy components
- **Virtual Scrolling**: Large list performance
- **Debounced Search**: Optimized search input

### Bundle Analysis

```bash
# Analyze bundle
npm run build
npm run analyze

# Bundle size monitoring
npm run build:analyze
```

## 🔧 Development

### Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run type-check

# Format code
npm run format
```

### Pre-commit Hooks

```bash
# Install husky
npm run prepare

# Pre-commit checks
npm run lint-staged
```

### Development Tools

- **React DevTools**: Component inspection
- **Redux DevTools**: State management debugging
- **React Query DevTools**: Server state monitoring
- **Storybook**: Component development and testing

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile first approach */
.sm: '640px'    /* Small devices */
.md: '768px'    /* Medium devices */
.lg: '1024px'   /* Large devices */
.xl: '1280px'   /* Extra large devices */
.2xl: '1536px'  /* 2X large devices */
```

### Mobile Optimizations

- **Touch-friendly**: Proper touch targets (44px+)
- **Gesture Support**: Swipe navigation and actions
- **Performance**: Optimized for mobile devices
- **Offline First**: Works without internet connection

## 🌐 SEO & Accessibility

### SEO Features

- **Meta Tags**: Dynamic meta information
- **Open Graph**: Social media sharing
- **Structured Data**: Schema.org markup
- **Sitemap**: Automatic sitemap generation

### Accessibility

- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard accessibility
- **Color Contrast**: WCAG AA compliance
- **Focus Management**: Proper focus indicators

## 🚀 Deployment

### Build Process

```bash
# Production build
npm run build

# Start production server
npm start

# Export static files
npm run export
```

### Environment Configuration

```bash
# Production environment
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.homlo.pk
NEXT_PUBLIC_WS_URL=wss://api.homlo.pk
```

### Deployment Options

- **Vercel**: Zero-config deployment
- **Netlify**: Static site hosting
- **AWS**: S3 + CloudFront
- **Docker**: Containerized deployment

## 🔗 API Integration

### React Query Setup

```tsx
// Query client configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

// API hooks
const { data: listings, isLoading } = useQuery({
  queryKey: ['listings', filters],
  queryFn: () => api.getListings(filters),
});
```

### Error Handling

```tsx
// Global error boundary
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>

// API error handling
const { data, error, isError } = useQuery({
  queryKey: ['listings'],
  queryFn: api.getListings,
  retry: 3,
  onError: (error) => {
    toast.error('Failed to load listings');
    console.error(error);
  },
});
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Guidelines

- Follow TypeScript best practices
- Use functional components with hooks
- Write comprehensive tests
- Maintain accessibility standards
- Follow the established design system

## 📄 License

This project is proprietary software for commercial use.

## 🆘 Support

For technical support or questions:

- **Documentation**: Check the component stories
- **Issues**: Report bugs via GitHub Issues
- **Team**: Contact the development team

## 🔗 Related Links

- [Backend API](../api/README.md)
- [Project Documentation](../../README.md)
- [Docker Setup](../../docker-compose.yml)
- [Component Library](http://localhost:6006)
