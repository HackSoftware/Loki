def get_comment_and_code(comment):
    # TODO: Think for better way of selecting code
    for line in comment.splitlines():
        if line.startswith("#"):
            pass
    return comment
