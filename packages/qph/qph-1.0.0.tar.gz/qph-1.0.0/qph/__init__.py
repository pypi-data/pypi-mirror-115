def generate_html(filepath = "", content=""):  # sourcery no-metrics skip: merge-nested-ifs
    import subprocess
    import os
    
    generated_html = ""
    old_html = ""
    if filepath:
        old_html = open(filepath, "r").read()
    elif content:
        old_html = content
    else:
        return "<h2 align=\"center\">QPH ERROR: NO HTML INPUT</h2>"

    c = 0
    while c != len(old_html):
        if old_html[c] == '{':
            if old_html[c+1] == '$':
                if old_html[c+2:c+5] == "qph":
                    temp = ""
                    for i, iterator in enumerate(old_html[c+6:]):
                        if old_html[c+6:][i-2:i] == "$}":
                            # exec(generate_html(content=temp[:-7]))
                            open(".py", "w").write("""def html_print(tag, content, tag_class=\"\", tag_id=\"\", tag_style=\"\"):
    print(f"<{tag} class=\\\"{tag_class}\\\" id=\\\"{tag_id}\\\" style=\\\"{tag_style}\\\">{content}</{tag}>", end="")\n"""+temp[:-7])
                            command = f"python .py & del .py"
                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                            output, error = process.communicate()
                            generated_html += f"<h2 align=\"center\">QPH ERROR: {str(error)[2:-5]}</h2>" if error else str(output)[2:-1]
                            os.system("cls")
                            del output, error, process, command
                            c += len(temp)+5
                            temp = ""
                            break
                        else:
                            temp += iterator
        else:
            generated_html += old_html[c]
        c += 1

    return generated_html