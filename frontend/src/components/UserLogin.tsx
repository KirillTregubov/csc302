import { ArrowRightOnRectangleIcon } from '@heroicons/react/20/solid'

import { useToken } from 'lib/tokenContext'

const authEndpoint = 'https://accounts.spotify.com/authorize'
const redirectUri = 'http://localhost:5000/callback'
const clientId = 'f07ef9ab78224bd6b90ffeedcc2d014c'
const scopes = [
  // 'user-read-private',
  // 'user-read-email',
  'user-read-currently-playing',
  'user-read-recently-played',
  'user-library-read',
  'user-top-read',
  'user-modify-playback-state'

]

const login_url = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join(
  '%20'
)}&response_type=token&show_dialog=true`

const UserLogin: React.FC = () => {
  const { token, setToken } = useToken()

  const onClick = () => {
    if (token) {
      localStorage.removeItem('token')
      localStorage.removeItem('token_expires_in')
      window.location.reload()
      return
    }

    window.location.href = login_url
  }

  return (
    <div>
      <button
        className="inline-flex items-center gap-2 rounded-full bg-[#1DB954] py-1 px-3.5 font-semibold text-black duration-150 active:scale-[.97] active:bg-[#169c46] active:will-change-transform"
        onClick={onClick}>
        {token ? (
          <>
            Logout
            <ArrowRightOnRectangleIcon className="h-4 w-4" />
          </>
        ) : (
          <>
            Sign in with Spotify
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 256 256"
              width="1rem"
              height="1rem"
              preserveAspectRatio="xMidYMid"
              className="h-[21px] w-[21px]">
              <path
                fill="currentColor"
                d="M128 0C57.308 0 0 57.309 0 128c0 70.696 57.309 128 128 128 70.697 0 128-57.304 128-128C256 57.314 198.697.007 127.998.007l.001-.006Zm58.699 184.614c-2.293 3.76-7.215 4.952-10.975 2.644-30.053-18.357-67.885-22.515-112.44-12.335a7.981 7.981 0 0 1-9.552-6.007 7.968 7.968 0 0 1 6-9.553c48.76-11.14 90.583-6.344 124.323 14.276 3.76 2.308 4.952 7.215 2.644 10.975Zm15.667-34.853c-2.89 4.695-9.034 6.178-13.726 3.289-34.406-21.148-86.853-27.273-127.548-14.92-5.278 1.594-10.852-1.38-12.454-6.649-1.59-5.278 1.386-10.842 6.655-12.446 46.485-14.106 104.275-7.273 143.787 17.007 4.692 2.89 6.175 9.034 3.286 13.72v-.001Zm1.345-36.293C162.457 88.964 94.394 86.71 55.007 98.666c-6.325 1.918-13.014-1.653-14.93-7.978-1.917-6.328 1.65-13.012 7.98-14.935C93.27 62.027 168.434 64.68 215.929 92.876c5.702 3.376 7.566 10.724 4.188 16.405-3.362 5.69-10.73 7.565-16.4 4.187h-.006Z"
              />
            </svg>
          </>
        )}
      </button>
    </div>
  )
}

export default UserLogin
