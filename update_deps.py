import subprocess

# TIMEOUT = 30 # seconds

def update_yt_dlp(ytdlp_path: str) -> bool:
    """
    Returns: (success, message)
    success: True = updated / already up-to-date
             False = failed or nothing useful happened
    """
    print("Updating yt-dlp, please wait...")

    cmd = [ytdlp_path, "-U"]

    try:
        # capture_output=True is cleaner than streaming + easier to debug
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,           # prevent hanging forever
            encoding="utf-8",
            errors="replace"
        )

        output = result.stdout + result.stderr


        # Most important check: exit code
        if result.returncode == 0:
            if "Updated yt-dlp to" in output:
                print("yt-dlp was successfully updated!")
                return True

            if "yt-dlp is up to date" in output:
                print("ytd-dlp is already up to date.")
                return True

            if "You installed yt-dlp with a package manager" in output or \
               "package manager" in output.lower():
                print("yt-dlp says it was installed via package manager → cannot self-update.")
                return False

            print("Maybe yt-dlp was updated. Please try '--sync' again to verify...")
            # print(output)
            return True

        # ── Non-zero exit = failure ───────────────────────
        else:
            print(f"Update FAILED (exit code {result.returncode})")
            print("Output was:")
            print(output.strip() or "<no output>")

            if result.returncode == 100:
                print("Exit 100 → yt-dlp wants to restart itself (nightly/master channel?). Using the stable release is recommended.")
                # Could re-exec or warn user
                return False

            return False

    # except subprocess.TimeoutExpired:
    #     print(f"Update timed out after {TIMEOUT} seconds!")
    #     return False

    except FileNotFoundError:
        print(f"yt-dlp not found at: {ytdlp_path}")
        return False

    except Exception as e:
        print(f"Unexpected error during update: {e}")
        return False


def update_all(ytdlp_path):
    # @TODO: check if download path exists (if already set before)
    update_yt_dlp(ytdlp_path=ytdlp_path)