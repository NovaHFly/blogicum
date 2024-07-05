# Testing plan

## Route/url availability tests
1. Static pages must be available for everyone:
   1. Rules
   2. About
2. Authorization pages must be available for everyone:
   1. Register
   2. Login
   3. Logout
3. Home page, category pages, post details (except unpublished) must be available for everyone
4. All post methods must be available to at least authorized user:
   1. Profile edit
   2. Post create
   3. Comment add
5. Edit and delete methods must be available only to post/comment author
6. Unpublished posts must be available for author but unavailable for everyone else:
   1. Post was unpublished
   2. Post belongs to a category which was unpublished
   3. Post is not published yet (its pub_date is greater than now)