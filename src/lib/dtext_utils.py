from bs4 import BeautifulSoup

def replace_html_headers(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<h1>', 'h1. ')
    html = html.replace('</h1>', '\n')
    html = html.replace('<h2>', 'h2. ')
    html = html.replace('</h2>', '\n')
    html = html.replace('<h3>', 'h3. ')
    html = html.replace('</h3>', '\n')
    html = html.replace('<h4>', 'h4. ')
    html = html.replace('</h4>', '\n')
    html = html.replace('<h5>', 'h5. ')
    html = html.replace('</h5>', '\n')
    html = html.replace('<h6>', 'h5. ')
    html = html.replace('</h6>', '\n')
    print("Headers replaced:\n{0}".format(html))
    return html

def replace_html_bold(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<strong>', '[b]')
    html = html.replace('</strong>', '[/b]')
    html = html.replace('<b>', '[b]')
    html = html.replace('</b>', '[/b]')
    print
    return html

def replace_html_underline(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<u>', '[u]')
    html = html.replace('</u>', '[/u]')
    print("Underline replaced:\n{0}".format(html))
    return html

def replace_html_italics(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<i>', '[i]')
    html = html.replace('</i>', '[/i]')
    html = html.replace('<em>', '[i]')
    html = html.replace('</em>', '[/i]')
    print("Italics replaced:\n{0}".format(html))
    return html

def replace_html_strikethrough(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<s>', '[s]')
    html = html.replace('</s>', '[/s]')
    html = html.replace('<strike>', '[s]')
    html = html.replace('</strike>', '[/s]')
    print("Strikethrough replaced:\n{0}".format(html))
    return html

def replace_html_paragraphs(html: str) -> str:
    if not html:
            return ""
    
    html = html.replace('<p>', '')
    html = html.replace('</p>', '\n')
    print("Paragraphs replaced:\n{0}".format(html))
    return html

def html_links_to_dtext(html: str) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all links and replace them
    for link in soup.find_all('a'):
        href = link.get('href', '')
        text = link.get_text()
        
        if href and text:
            # Replace the link with DTEXT format
            link.replace_with(f'"{text}":{href}')
        else:
            # If no href or no text, just use the text content
            link.replace_with(text)
    
    # Return the modified HTML as string
    print("Links replaced:\n{0}".format(str(soup)))
    return str(soup)

def html_images_to_dtext(html: str) -> str:
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all images and replace them
    for img in soup.find_all('img'):
        src = img.get('src', '')
        
        if src:
            # Replace the image with DTEXT format
            img.replace_with(f'"(image)":{src}')
        else:
            # If no src, just remove the tag
            img.replace_with('')
    
    # Return the modified HTML as string
    print("Images replaced:\n{0}".format(str(soup)))
    return str(soup)

def convert_quotes_to_dtext(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<blockquote>', '[quote]')
    html = html.replace('</blockquote>', '[/quote]')
    print("Quotes replaced:\n{0}".format(html))
    return html

def convert_code_blocks_to_dtext(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<code>', '[code]')
    html = html.replace('</code>', '[/code]')
    print("Code blocks replaced:\n{0}".format(html))
    return html

def convert_tables_to_dtext(html: str) -> str:
    if not html:
            return ""
    html = html.replace('<table>', '[table]')
    html = html.replace('</table>', '[/table]')
    html = html.replace('<tr>', '[tr]')
    html = html.replace('</tr>', '[/tr]')
    html = html.replace('<td>', '[td]')
    html = html.replace('</td>', '[/td]')
    html = html.replace('<tbody>', '[tbody]')
    html = html.replace('</tbody>', '[/tbody]')
    html = html.replace('<thead>', '[thead]')
    html = html.replace('</thead>', '[/thead]')
    print("Tables replaced:\n{0}".format(html))
    return html

def convert_nested_lists_to_dtext(html: str) -> str:
    """
    Convert nested HTML lists (both <ul> and <ol>) to textile-style lists.
    
    Converts:
    <ul>
      <li>tier1</li>
      <li>
        <ul>
          <li>tier2</li>
          <ul>
            <li>tier3</li>
          </ul>
        </ul>
      </li>
    </ul>
    
    To:
    * tier1
    ** tier2
    *** tier3
    
    Both ordered and unordered lists are converted to unordered textile lists.
    Preserves all other HTML content.
    """
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    def process_list(element, level=1):
        """Recursively process lists and return textile-formatted text."""
        result = []
        for child in element.children:
            if child.name == 'li':
                # Get the text content of the li, excluding nested lists
                text_parts = []
                for item in child.children:
                    if isinstance(item, str):
                        text_parts.append(str(item).strip())
                    elif hasattr(item, 'name') and item.name not in ['ul', 'ol']:
                        text_parts.append(item.get_text().strip())
                
                text_content = ''.join(text_parts).strip()
                if text_content:
                    result.append('*' * level + ' ' + text_content)
                
                # Process nested lists inside this li
                for nested_list in child.find_all(['ul', 'ol'], recursive=False):
                    result.extend(process_list(nested_list, level + 1))
            elif child.name in ['ul', 'ol']:
                # Nested list that's a sibling (not inside li)
                result.extend(process_list(child, level + 1))
        
        return result
    
    # Find all top-level lists and replace them with textile output
    lists = soup.find_all(['ul', 'ol'], recursive=False)
    if lists:
        for list_element in lists:
            textile_lines = process_list(list_element, 1)
            if textile_lines:
                textile_text = '\n'.join(textile_lines)
                print("Nested lists replaced:\n{0}".format(textile_text))
                # Replace with textile text and add newlines for spacing
                list_element.replace_with('\n' + textile_text + '\n')
        
        # Return the modified HTML
        html = str(soup)
        print("Lists replaced:\n{0}".format(html))
        return html
    else:
        # No lists found, return original HTML
        print("No lists found:\n{0}".format(html))
        return html





def convert_to_dtext(html: str) -> str:
    if not html:
         return ""
    # Process lists first before other conversions
    html = convert_nested_lists_to_dtext(html)
    html = replace_html_headers(html)
    html = replace_html_bold(html)
    html = replace_html_italics(html)
    html = replace_html_underline(html)
    html = html_links_to_dtext(html)
    html = html_images_to_dtext(html)
    html = replace_html_paragraphs(html)
    html = replace_html_strikethrough(html)
    html = convert_quotes_to_dtext(html)
    html = convert_code_blocks_to_dtext(html)
    html = convert_tables_to_dtext(html)
    return html