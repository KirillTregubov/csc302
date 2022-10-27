import {
  QueryClientProvider,
  QueryClient
  // useQuery
} from '@tanstack/react-query'

// import QueryInput from 'components/QueryInput'
// import RecommendedTracks from 'components/RecommendedTracks'
import SpotifySearch from 'components/SpotifySearch'
// import { getDemoQuery } from 'lib/api'

const App: React.FC = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false
      }
    }
  })

  return (
    <QueryClientProvider client={queryClient}>
      <div id="App" className="m-2">
        <p>Hello from App.tsx</p>
        <SpotifySearch />
        {/* <QueryInput />
        <Fetch /> */}
        {/* <RecommendedTracks /> */}
      </div>
    </QueryClientProvider>
  )
}

export default App
