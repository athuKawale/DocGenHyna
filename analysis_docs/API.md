Now I have enough information to generate comprehensive API documentation. Let me create the API.md file:

# API.md

## Overview

This document provides comprehensive API documentation for the backend streaming platform. The system is built with a modular architecture featuring Redux state management, RESTful API services, and a media player system.

---

## Table of Contents

1. [API Services](#api-services)
2. [Redux Store & State Management](#redux-store--state-management)
3. [Custom Hooks](#custom-hooks)
4. [Media Player API](#media-player-api)
5. [Data Types](#data-types)
6. [Error Handling](#error-handling)
7. [Configuration](#configuration)

---

## API Services

### Base Configuration

#### `createRestClient()`
**Location:** `src/api/restClient.ts`

Creates and configures the HTTP client for all API requests.

**Returns:**
- HTTP client instance with interceptors configured

**Features:**
- Device header injection via `deviceHeaderInterceptor()`
- Base URL configuration from environment
- Response error handling

---

### Platform Service

#### `getPlatforms()`
**Location:** `src/api/services/platformService.ts`

Retrieves available streaming platforms.

**Parameters:** None

**Returns:**
```typescript
Promise<Platform[]>
```

**Usage:**
```typescript
const platforms = await getPlatforms();
```

---

### Favorites Service

**Location:** `src/api/services/favoritesService.ts`

#### `getFavorites()`
Retrieves user's favorite items.

**Parameters:** None

**Returns:**
```typescript
Promise<Favorite[]>
```

#### `addFavorite(itemId: string)`
Adds an item to favorites.

**Parameters:**
- `itemId` (string): ID of the item to favorite

**Returns:**
```typescript
Promise<void>
```

**Errors:**
- Network error
- Invalid item ID

#### `removeFavorite(itemId: string)`
Removes an item from favorites.

**Parameters:**
- `itemId` (string): ID of the item to remove

**Returns:**
```typescript
Promise<void>
```

#### `buildFavoritesEndpoint()`
Helper function to construct favorites API endpoint.

**Returns:**
```typescript
string
```

---

### Home Content Service

**Location:** `src/api/services/homeService.ts`

#### `getHomeContent()`
Retrieves home screen content including banners and categories.

**Parameters:** None

**Returns:**
```typescript
Promise<HomeContent>
```

**Response Structure:**
```typescript
{
  banners: Banner[],
  categories: Category[],
  continueWatching: Video[]
}
```

#### `getHomeViewAll(categoryId: string, page: number)`
Retrieves all items in a specific home category with pagination.

**Parameters:**
- `categoryId` (string): Category identifier
- `page` (number): Page number for pagination

**Returns:**
```typescript
Promise<PaginatedResponse<Video>>
```

---

### Videos Service

**Location:** `src/api/services/videosService.ts`

#### `getVideos()`
Retrieves all available videos with categories.

**Parameters:** None

**Returns:**
```typescript
Promise<VideosResponse>
```

**Response Structure:**
```typescript
{
  categories: VideoCategory[],
  videos: Video[]
}
```

#### `getVideosByCategory(categoryId: string, page: number)`
Retrieves videos filtered by category.

**Parameters:**
- `categoryId` (string): Category identifier
- `page` (number): Page number for pagination

**Returns:**
```typescript
Promise<PaginatedResponse<Video>>
```

#### `getVideosAll(page: number)`
Retrieves all videos with pagination.

**Parameters:**
- `page` (number): Page number for pagination

**Returns:**
```typescript
Promise<PaginatedResponse<Video>>
```

---

### TV Shows Service

**Location:** `src/api/services/tvShowsService.ts`

#### `getTvShows()`
Retrieves all TV shows with categories.

**Parameters:** None

**Returns:**
```typescript
Promise<TvShowsResponse>
```

**Response Structure:**
```typescript
{
  categories: TvShowCategory[],
  shows: TvShow[]
}
```

#### `getTvShowEpisodes(showId: string)`
Retrieves episodes for a specific TV show.

**Parameters:**
- `showId` (string): TV show identifier

**Returns:**
```typescript
Promise<Episode[]>
```

#### `getTvShowEpisodesStag(showId: string)`
Retrieves staged/upcoming episodes for a TV show.

**Parameters:**
- `showId` (string): TV show identifier

**Returns:**
```typescript
Promise<Episode[]>
```

---

### Detail Service

**Location:** `src/api/services/detailService.ts`

#### `getVideoDetail(videoId: string)`
Retrieves detailed information about a specific video.

**Parameters:**
- `videoId` (string): Video identifier

**Returns:**
```typescript
Promise<VideoDetail>
```

**Response Structure:**
```typescript
{
  id: string,
  title: string,
  description: string,
  duration: number,
  releaseDate: string,
  genres: string[],
  cast: string[],
  relatedVideos: Video[],
  playbackUrl: string,
  subtitles: Subtitle[]
}
```

#### `getTvShowEpisodeDetail(episodeId: string)`
Retrieves detailed information about a TV show episode.

**Parameters:**
- `episodeId` (string): Episode identifier

**Returns:**
```typescript
Promise<EpisodeDetail>
```

---

### Search Service

**Location:** `src/api/services/searchService.ts`

#### `search(query: string, page: number)`
Searches for videos and shows.

**Parameters:**
- `query` (string): Search query string
- `page` (number): Page number for pagination

**Returns:**
```typescript
Promise<SearchResults>
```

**Response Structure:**
```typescript
{
  results: SearchItem[],
  totalResults: number,
  currentPage: number,
  hasMore: boolean
}
```

---

### View All Service

**Location:** `src/api/services/viewAllService.ts`

#### `getViewAll(categoryId: string, page: number)`
Retrieves all items in a category with pagination.

**Parameters:**
- `categoryId` (string): Category identifier
- `page` (number): Page number for pagination

**Returns:**
```typescript
Promise<PaginatedResponse<Item>>
```

---

### Endpoints Configuration

**Location:** `src/api/endpoints.ts`

#### `buildQueryString(params: Record<string, any>)`
Constructs URL query string from parameters.

**Parameters:**
- `params` (object): Key-value pairs for query parameters

**Returns:**
```typescript
string
```

**Example:**
```typescript
buildQueryString({ page: 1, limit: 20 })
// Returns: "?page=1&limit=20"
```

---

## Redux Store & State Management

### Store Configuration

**Location:** `src/store/store.ts`

#### `useAppDispatch()`
Redux dispatch hook for triggering actions across all slices.

**Returns:**
```typescript
AppDispatch
```

**Usage:**
```typescript
const dispatch = useAppDispatch();
dispatch(someAction());
```

---

### Player Slice

**Location:** `src/store/slices/playerSlice.ts`

#### Selectors

- `selectIsPlaying()` - Returns current playback state
- `selectCurrentPosition()` - Returns current playback position in seconds
- `selectDuration()` - Returns total video duration in seconds
- `selectIsBuffering()` - Returns buffering state
- `selectPlayerError()` - Returns any player errors
- `selectAvailableQualities()` - Returns available video qualities
- `selectSelectedQuality()` - Returns currently selected quality
- `selectPlaybackSpeed()` - Returns current playback speed
- `selectAvailableSubtitles()` - Returns available subtitle tracks
- `selectSelectedSubtitle()` - Returns currently selected subtitle

---

### Home Slice

**Location:** `src/store/slices/homeSlice.ts`

#### Selectors

- `selectHomeBanners()` - Returns home screen banners
- `selectHomeCategories()` - Returns home content categories
- `selectHomeLoading()` - Returns loading state
- `selectHomeError()` - Returns any errors
- `selectContinueWatchingWithProgress()` - Returns continue watching items with progress

---

### TV Shows Slice

**Location:** `src/store/slices/tvShowsSlice.ts`

#### Selectors

- `selectTvShowsCategories()` - Returns TV show categories
- `selectTvShowsBanner()` - Returns TV shows banner
- `selectTvShowsLoading()` - Returns loading state
- `selectTvShowsError()` - Returns any errors
- `selectEpisodesByShowId(showId)` - Returns episodes for a show
- `selectEpisodeBannerByShowId(showId)` - Returns episode banner for a show
- `selectTvShowsEpisodesLoading()` - Returns episodes loading state

---

### Videos Slice

**Location:** `src/store/slices/videosSlice.ts`

#### Selectors

- `selectVideosCategories()` - Returns video categories
- `selectVideosLoading()` - Returns loading state
- `selectVideosError()` - Returns any errors

---

### Detail Slice

**Location:** `src/store/slices/detailSlice.ts`

#### Selectors

- `selectCurrentDetail()` - Returns current video/episode details
- `selectDetailLoading()` - Returns loading state
- `selectDetailError()` - Returns any errors
- `selectRelatedVideos()` - Returns related video recommendations
- `selectRelatedTitle()` - Returns related content title

---

### Search Slice

**Location:** `src/store/slices/searchSlice.ts`

#### Selectors

- `selectSearchQuery()` - Returns current search query
- `selectSearchResults()` - Returns search results
- `selectSearchLoading()` - Returns loading state
- `selectSearchError()` - Returns any errors
- `selectSearchHasMore()` - Returns if more results available
- `selectSearchCurrentPage()` - Returns current page number

---

### Favorites Slice

**Location:** `src/store/slices/favoritesSlice.ts`

#### Selectors

- `selectFavoriteIds()` - Returns array of favorite item IDs
- `selectIsFavorite(itemId)` - Returns if item is favorited
- `selectFavoritesLoading()` - Returns loading state

---

### Watch History Slice

**Location:** `src/store/slices/watchHistorySlice.ts`

#### Selectors

- `selectWatchHistoryEntries()` - Returns watch history entries
- `selectWatchHistoryEntriesArray()` - Returns watch history as array
- `selectWatchEntryById(entryId)` - Returns specific watch entry
- `selectResumePosition()` - Returns resume position for current video
- `selectWatchHistoryLoading()` - Returns loading state

---

### View All Slice

**Location:** `src/store/slices/viewAllSlice.ts`

#### Selectors

- `selectViewAllItems()` - Returns paginated items
- `selectViewAllCurrentPage()` - Returns current page
- `selectViewAllHasMore()` - Returns if more items available
- `selectViewAllLoading()` - Returns loading state
- `selectViewAllError()` - Returns any errors

---

### Platform Slice

**Location:** `src/store/slices/platformSlice.ts`

#### Selectors

- `selectHasPlatform()` - Returns if platform is selected
- `selectPlatform()` - Returns current platform

---

### Settings Slice

**Location:** `src/store/slices/settingsSlice.ts`

#### Selectors

- `selectSettings()` - Returns user settings
- `selectTheme()` - Returns current theme preference

---

## Custom Hooks

### `useAppDispatch()`
**Location:** `src/store/store.ts`

Provides access to Redux dispatch function.

**Returns:**
```typescript
AppDispatch
```

---

### `usePlayer()`
**Location:** `src/hooks/usePlayer.ts`

Manages video player state and controls.

**Returns:**
```typescript
{
  isPlaying: boolean,
  currentPosition: number,
  duration: number,
  isBuffering: boolean,
  error: string | null,
  availableQualities: Quality[],
  selectedQuality: Quality,
  playbackSpeed: number,
  availableSubtitles: Subtitle[],
  selectedSubtitle: Subtitle | null
}
```

---

### `useWatchHistory()`
**Location:** `src/hooks/useWatchHistory.ts`

Manages watch history and resume positions.

**Returns:**
```typescript
{
  entries: WatchHistoryEntry[],
  resumePosition: number,
  loading: boolean
}
```

---

### `useFavorites()`
**Location:** `src/hooks/useFavorites.ts`

Manages user's favorite items.

**Returns:**
```typescript
{
  favoriteIds: string[],
  isFavorite: (itemId: string) => boolean,
  loading: boolean
}
```

---

### `useHomeContent()`
**Location:** `src/hooks/useHomeContent.ts`

Fetches and manages home screen content.

**Returns:**
```typescript
{
  banners: Banner[],
  categories: Category[],
  continueWatching: Video[],
  loading: boolean,
  error: string | null
}
```

---

### `useVideos()`
**Location:** `src/hooks/useVideos.ts`

Manages video content and categories.

**Returns:**
```typescript
{
  categories: VideoCategory[],
  loading: boolean,
  error: string | null
}
```

---

### `useTvShows()`
**Location:** `src/hooks/useTvShows.ts`

Manages TV shows and categories.

**Returns:**
```typescript
{
  categories: TvShowCategory[],
  banner: Banner,
  loading: boolean,
  error: string | null
}
```

---

### `useTvShowEpisodes(showId: string)`
**Location:** `src/hooks/useTvShows.ts`

Fetches episodes for a specific TV show.

**Parameters:**
- `showId` (string): TV show identifier

**Returns:**
```typescript
{
  episodes: Episode[],
  banner: Banner,
  loading: boolean
}
```

---

### `useVideoDetail(videoId: string)`
**Location:** `src/hooks/useVideoDetail.ts`

Fetches detailed information about a video.

**Parameters:**
- `videoId` (string): Video identifier

**Returns:**
```typescript
{
  detail: VideoDetail,
  relatedVideos: Video[],
  relatedTitle: string,
  loading: boolean,
  error: string | null
}
```

---

### `useSearch(query: string, page: number)`
**Location:** `src/hooks/useSearch.ts`

Performs search operations.

**Parameters:**
- `query` (string): Search query
- `page` (number): Page number

**Returns:**
```typescript
{
  results: SearchItem[],
  loading: boolean,
  error: string | null,
  hasMore: boolean,
  currentPage: number
}
```

---

### `useViewAll(categoryId: string, page: number)`
**Location:** `src/hooks/useViewAll.ts`

Fetches paginated items from a category.

**Parameters:**
- `categoryId` (string): Category identifier
- `page` (number): Page number

**Returns:**
```typescript
{
  items: Item[],
  currentPage: number,
  hasMore: boolean,
  loading: boolean,
  error: string | null
}
```

---

### `usePlatformSelection()`
**Location:** `src/hooks/usePlatformSelection.ts`

Manages platform selection.

**Returns:**
```typescript
{
  selectedPlatform: Platform | null,
  hasPlatform: boolean
}
```

---

### `useSettings()`
**Location:** `src/hooks/useSettings.ts`

Manages user settings.

**Returns:**
```typescript
{
  settings: UserSettings,
  theme: 'light' | 'dark'
}
```

---

### `useBackHandler()`
**Location:** `src/hooks/useBackHandler.ts`

Handles back button navigation.

**Returns:**
```typescript
void
```

---

### `useFocusAnimation()`
**Location:** `src/hooks/useFocusAnimation.ts`

Manages focus animation for TV/remote navigation.

**Returns:**
```typescript
{
  animatedValue: Animated.Value,
  onFocus: () => void,
  onBlur: () => void
}
```

---

## Media Player API

### ShakaPlayer

**Location:** `src/w3cmedia/ShakaPlayer.ts`

Advanced media player implementation using Shaka Player.

#### Constructor
```typescript
new ShakaPlayer(videoElement: HTMLVideoElement)
```

#### Methods

##### `load(manifestUrl: string, options?: LoadOptions)`
Loads a media manifest (DASH/HLS).

**Parameters:**
- `manifestUrl` (string): URL to media manifest
- `options` (optional): Load configuration

**Returns:**
```typescript
Promise<void>
```

##### `play()`
Starts playback.

**Returns:**
```typescript
Promise<void>
```

##### `pause()`
Pauses playback.

**Returns:**
```typescript
Promise<void>
```

##### `seekBack(seconds: number = 10)`
Seeks backward in the video.

**Parameters:**
- `seconds` (number): Seconds to seek back (default: 10)

**Returns:**
```typescript
void
```

##### `seekFront(seconds: number = 10)`
Seeks forward in the video.

**Parameters:**
- `seconds` (number): Seconds to seek forward (default: 10)

**Returns:**
```typescript
void
```

##### `unload()`
Unloads current media.

**Returns:**
```typescript
Promise<void>
```

#### Request/Response Filters

##### `uplynkRequestFilter(type: string, request: Request)`
Filters requests for Uplynk CDN.

##### `uplynkResponseFilter(type: string, response: Response)`
Filters responses from Uplynk CDN.

##### `addManifestRequestHeaders_()`
Adds custom headers to manifest requests.

##### `addLicenseRequestHeaders_()`
Adds custom headers to license requests.

---

### VideoHandler

**Location:** `src/utils/VideoHandler.ts`

Manages video playback and media controls.

#### Constructor
```typescript
new VideoHandler(videoElement: HTMLVideoElement, player: ShakaPlayer)
```

#### Methods

##### `setMediaData(mediaData: MediaData)`
Sets media information for playback.

**Parameters:**
```typescript
{
  id: string,
  title: string,
  duration: number,
  playbackUrl: string,
  subtitles?: Subtitle[],
  qualities?: Quality[]
}
```

##### `preBufferVideo()`
Pre-buffers video content.

**Returns:**
```typescript
Promise<void>
```

##### `loadVideoElements()`
Initializes video DOM elements.

**Returns:**
```typescript
void
```

##### `loadStaticMediaPlayer()`
Loads static media player configuration.

**Returns:**
```typescript
Promise<void>
```

##### `loadAdaptiveMediaPlayer()`
Loads adaptive bitrate streaming configuration.

**Returns:**
```typescript
Promise<void>
```

##### `loadSubtitles(subtitles: Subtitle[])`
Loads subtitle tracks.

**Parameters:**
- `subtitles` (array): Array of subtitle objects

**Returns:**
```typescript
Promise<void>
```

##### `setupEventListeners()`
Attaches event listeners to player.

**Returns:**
```typescript
void
```

##### `removeEventListeners()`
Removes event listeners from player.

**Returns:**
```typescript
void
```

##### `destroyMediaPlayerSync()`
Synchronously destroys media player.

**Returns:**
```typescript
void
```

##### `destroyVideoElements()`
Removes video DOM elements.

**Returns:**
```typescript
void
```

---

### AppOverrideMediaControlHandler

**Location:** `src/utils/VideoHandler.ts`

Handles media control commands (play, pause, seek, etc.).

#### Methods

##### `handlePlay()`
Handles play command.

##### `handlePause()`
Handles pause command.

##### `handleTogglePlayPause()`
Toggles between play and pause.

##### `handleStop()`
Handles stop command.

##### `handleStartOver()`
Restarts video from beginning.

##### `handleRewind(seconds: number = 10)`
Rewinds video.

**Parameters:**
- `seconds` (number): Seconds to rewind

##### `handleFastForward(seconds: number = 10)`
Fast forwards video.

**Parameters:**
- `seconds` (number): Seconds to fast forward

##### `handleSeek(position: number)`
Seeks to specific position.

**Parameters:**
- `position` (number): Position in seconds

---

## Data Types

### Common Types

#### Video
```typescript
{
  id: string,
  title: string,
  description: string,
  thumbnail: string,
  duration: number,
  releaseDate: string,
  genres: string[],
  rating: number
}
```

#### VideoDetail
```typescript
{
  id: string,
  title: string,
  description: string,
  duration: number,
  releaseDate: string,
  genres: string[],
  cast: string[],
  director: string,
  rating: number,
  playbackUrl: string,
  subtitles: Subtitle[],
  qualities: Quality[],
  relatedVideos: Video[]
}
```

#### TvShow
```typescript
{
  id: string,
  title: string,
  description: string,
  thumbnail: string,
  totalEpisodes: number,
  genres: string[],
  rating: number
}
```

#### Episode
```typescript
{
  id: string,
  showId: string,
  title: string,
  description: string,
  episodeNumber: number,
  seasonNumber: number,
  duration: number,
  releaseDate: string,
  thumbnail: string,
  playbackUrl: string
}
```

#### Subtitle
```typescript
{
  id: string,
  language: string,
  url: string,
  format: 'vtt' | 'srt' | 'ttml'
}
```

#### Quality
```typescript
{
  id: string,
  resolution: string,
  bitrate: number,
  label: string
}
```

#### Banner
```typescript
{
  id: string,
  title: string,
  image: string,
  link: string,
  priority: number
}
```

#### Category
```typescript
{
  id: string,
  name: string,
  description: string,
  thumbnail: string,
  itemCount: number
}
```

#### Platform
```typescript
{
  id: string,
  name: string,
  logo: string,
  isActive: boolean
}
```

#### WatchHistoryEntry
```typescript
{
  id: string,
  videoId: string,
  title: string,
  thumbnail: string,
  resumePosition: number,
  duration: number,
  watchedAt: string
}
```

#### SearchItem
```typescript
{
  id: string,
  type: 'video' | 'show' | 'episode',
  title: string,
  description: string,
  thumbnail: string,
  rating: number
}
```

#### PaginatedResponse
```typescript
{
  items: T[],
  currentPage: number,
  totalPages: number,
  totalItems: number,
  hasMore: boolean
}
```

---

## Error Handling

### Response Interceptor

**Location:** `src/api/interceptors/responseInterceptor.ts`

#### `isSuccessStatus(status: number)`
Checks if HTTP status indicates success.

**Parameters:**
- `status` (number): HTTP status code

**Returns:**
```typescript
boolean
```

#### `createApiError(response: Response)`
Creates standardized API error object.

**Parameters:**
- `response` (Response): HTTP response object

**Returns:**
```typescript
{
  message: string,
  status: number,
  code: string,
  details?: any
}
```

### Error Types

#### ApiError
```typescript
{
  message: string,
  status: number,
  code: string,
  details?: Record<string, any>
}
```

#### Common Error Codes
- `NETWORK_ERROR` - Network connectivity issue
- `UNAUTHORIZED` - Authentication required
- `FORBIDDEN` - Access denied
- `NOT_FOUND` - Resource not found
- `SERVER_ERROR` - Server error
- `INVALID_REQUEST` - Invalid request parameters
- `TIMEOUT` - Request timeout

---

## Configuration

### Environment Configuration

**Location:** `src/config/env.ts`

#### `getBaseUrl()`
Returns the API base URL.

**Returns:**
```typescript
string
```

**Environment Variables:**
- `REACT_APP_API_BASE_URL` - API base URL
- `REACT_APP_ENVIRONMENT` - Environment (development/production)

---

### Device Header Interceptor

**Location:** `src/api/interceptors/deviceHeaderInterceptor.ts`

#### `deviceHeaderInterceptor()`
Adds device-specific headers to all requests.

**Headers Added:**
- `X-Device-Type` - Device type identifier
- `X-Device-Model` - Device model
- `X-App-Version` - Application version
- `X-Platform` - Platform identifier

---

### Theme Configuration

**Location:** `src/config/theme.ts`

#### `useTheme()`
Provides theme configuration and utilities.

**Returns:**
```typescript
{
  colors: ThemeColors,
  spacing: SpacingScale,
  typography: TypographyConfig,
  isDark: boolean
}
```

---

## Usage Examples

### Fetching Video Details
```typescript
import { useVideoDetail } from 'src/hooks/useVideoDetail';

function VideoDetailComponent({ videoId }) {
  const { detail, relatedVideos, loading, error } = useVideoDetail(videoId);
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <div>
      <h1>{detail.title}</h1>
      <VideoPlayer url={detail.playbackUrl} />
      <RelatedVideos videos={relatedVideos} />
    </div>
  );
}
```

### Managing Favorites
```typescript
import { useFavorites } from 'src/hooks/useFavorites';

function FavoriteButton({ videoId }) {
  const { isFavorite, loading } = useFavorites();
  const dispatch = useAppDispatch();
  
  const handleToggleFavorite = async () => {
    if (isFavorite(videoId)) {
      await dispatch(removeFavorite(videoId));
    } else {
      await dispatch(addFavorite(videoId));
    }
  };
  
  return (
    <button onClick={handleToggleFavorite} disabled={loading}>
      {isFavorite(videoId) ? '★ Favorited' : '☆ Add to Favorites'}
    </button>
  );
}
```

### Searching Content
```typescript
import { useSearch } from 'src/hooks/useSearch';

function SearchComponent() {
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(1);
  const { results, loading, hasMore } = useSearch(query, page);
  
  return (
    <div>
      <input 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search videos..."
      />
      <SearchResults items={results} />
      {hasMore && (
        <button onClick={() => setPage(page + 1)}>Load More</button>
      )}
    </div>
  );
}
```

### Playing Video
```typescript
import { usePlayer } from 'src/hooks/usePlayer';
import { VideoHandler } from 'src/utils/VideoHandler';

function PlayerComponent({ videoId }) {
  const videoRef = useRef(null);
  const { isPlaying, currentPosition } = usePlayer();
  
  useEffect(() => {
    const handler = new VideoHandler(videoRef.current, new ShakaPlayer(videoRef.current));
    handler.setMediaData({
      id: videoId,
      title: 'Video Title',
      duration: 3600,
      playbackUrl: 'https://example.com/manifest.mpd'
    });
  }, [videoId]);
  
  return <video ref={videoRef} />;
}
```

---

## API Rate Limiting

The API implements standard rate limiting:
- **Default Limit:** 100 requests per minute per IP
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Versioning

Current API Version: **1.0.0**

---

## Support

For API issues or questions, please refer to the internal documentation or contact the development team.