# sitemap-checker

### Microsoft Teams integrated sitemap smoke tester.

Tests each url in specified sitemap and sends message to a channel in Teams.
This script only checks whether http response code is 200 or not.

- Sitemap.xml file url is read from SITEMAP_URL environment variable.
- Channel incoming web hook url is read from WEBHOOK_URL environment variable.
