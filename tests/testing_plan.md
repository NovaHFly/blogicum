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

## Content tests
1. All pages with paginators must contain a set count of posts per page.
2. Posts must display in order from newest to oldest
3. Comments must display in order from oldest to newest
4. Post detail page must contain comment form for authorized users
5. Correct forms are passed to post add/edit, comment edit and profile edit pages.
6. Unpublished posts do not show in home page and category pages
7. Unpublished posts show in profile for their author and do not show for everyone else

## Logic tests
1. Anonymous user can't create posts nor add comments
2. Authorized user can do all of the above
3. Only author can edit and delete their posts and comments

# Test groups
1. App_Blog
   1. Posts
   2. Comments
   3. Unpublished posts
2. Static pages
3. Auth routes