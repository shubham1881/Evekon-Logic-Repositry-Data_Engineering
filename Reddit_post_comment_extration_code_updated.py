import praw
import time

reddit = praw.Reddit(client_id='your app id ',
                     client_secret='your app secre',
                     user_agent = 'app_name/v1.0 (by u/username)')

# Infinite loop to keep reading and processing post IDs
while True:
    print('Reading post IDs from file...')
    # Read post IDs from file
    with open('post_ids.txt', 'r') as f:
        post_ids = [line.strip() for line in f]

    # Create text file for all comments
    print('Creating text file for comments...')
    with open('comments.txt', 'w', encoding='utf-8') as f:
        # Iterate over post IDs in reverse order and extract comments
        for post_id in reversed(post_ids):
            print(f'Extracting comments from post ID: {post_id}')
            # Load post from ID
            post = reddit.submission(id=post_id)
            # Get the 6 newest comments in reverse order
            comments = post.comments.list()[-6:][::-1]
            # Write post ID to file
            f.write(f'{post_id};')
            # Write each comment to file
            for comment in comments:
                # Check if comment is an instance of Comment
                if isinstance(comment, praw.models.Comment):
                    comment_body = comment.body.replace(';', '').replace('\n', 'n/')
                    try:
                        f.write(f'{comment_body};')
                    except UnicodeEncodeError:
                        # Handle UnicodeEncodeError exception by encoding as ASCII and ignoring errors
                        f.write(f'{comment_body.encode("ascii", "ignore").decode("ascii")};')
            f.write('\n')
    
    # Wait for 10 seconds before processing the next batch of posts
    print('Sleeping for 10 seconds...')
    time.sleep(10)