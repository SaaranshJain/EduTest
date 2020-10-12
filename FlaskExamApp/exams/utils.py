GROUP_NAMES = (
    'plain',
    'q',
    'mcq',
    'text',
    'image',
    'checkbox',
    'match',
    'code'
)


class SpecialTagParsers():

    @staticmethod
    def get_tags_from_text(pattern, text: str) -> list:
        import re

        all_tags = []

        for match_object in re.finditer(pattern, text):
            loc = (match_object.start(), match_object.end())
            all_tags.append({'loc': loc})

        return all_tags

    @staticmethod
    def mcq(text):
        tags = SpecialTagParsers.get_tags_from_text(r'#\d+', text)

        mcq_list = []

        if not tags:
            raise ValueError(
                'Multiple Choice Question cannot have zero options'
            )

        # all except last tag
        for index, tag in enumerate(tags[:-1]):
            mcq_list.append(
                text[tag['loc'][1]:tags[index+1]['loc'][0]].strip()
            )

        # last tag
        mcq_list.append(text[tags[-1]['loc'][1]:].strip())

        return mcq_list

    @staticmethod
    def match(text):
        # can use SpecialTagParsers.mcq for each set of options
        block_tags = SpecialTagParsers.get_tags_from_text(
            r'\[[a-zA-Z]\]',
            text
        )
        if not block_tags:
            raise ValueError(
                'Cannot create a matching question with no blocks'
            )

        if len(block_tags) != 2:
            raise ValueError(
                f'''Cannot create a matching question with {len(block_tags)} blocks.
                Please change the question to have only two blocks'''
            )

        block_list = {
            'A': text[block_tags[0]['loc'][1]:block_tags[1]['loc'][0]],
            'B': text[block_tags[1]['loc'][1]:]
        }

        for block in block_list.keys():
            block_list[block] = SpecialTagParsers.mcq(block_list[block])

        return block_list


def get_text_from_file(full_filename: str) -> str:
    '''
    Read and return the text data of the given file
    '''
    import os
    _, ext = os.path.splitext(full_filename)

    text = None
    # read file according to file type
    if ext == '.txt':
        # if file is a .txt file, simply open and read it
        with open(full_filename, 'r+') as file:
            text = file.read().replace(r'\n\n', '\n')

    elif ext == '.docx':
        # .docx files can be read by joining their paragraphs eith newlines
        from docx import Document
        file = Document(full_filename)
        text = '\n'.join(para.text for para in file.paragraphs)
    else:
        # other extensions that are not yet supported
        raise ValueError(f'This program does not support files of {ext} type.')

    # if, for some reason text is falsy, but not an empty string
    if not text and text != '':
        raise RuntimeError(
            'Something went wrong while trying to read the document'
        )

    return text


def get_tags_from_text(text: str) -> list:
    import re

    all_tags = []

    for match_object in re.finditer(r'<\w+>', text):
        loc = (match_object.start(), match_object.end())
        single_tag = text[loc[0]: loc[1]]

        if single_tag.strip('<>') not in GROUP_NAMES:
            raise ValueError(f'The tag {single_tag} does not exist.')
        else:
            all_tags.append({'name': single_tag.strip('<>'), 'loc': loc})
    return all_tags


def parse_to_groups(text: str, tags: list) -> list:
    '''
    Receive text input and parse into groups.
    '''
    groups = []

    # if there are no tags
    if not tags:
        groups.append({
            'type': 'plain',
            'value': text
        })

        return groups

    # in case first group doesn't start at the beginning of the string
    if tags[0]['loc'][0] != 0:
        groups.append({
            'type': 'plain',
            'value': text[: tags[0]['loc'][0]].strip()
        })

    # all tags except last
    for index, tag in enumerate(tags[:-1]):
        groups.append({
            'type': tag['name'],
            'value': text[tag['loc'][1]:tags[index+1]['loc'][0]].strip()
        })

    # last tag
    groups.append({
        'type': tags[-1]['name'],
        'value': text[tags[-1]['loc'][1]:].strip()
    })

    return groups


def parse_document(full_filename: str) -> list:
    '''
    Receive a text filename and parse into a list in order to create a form
    '''
    text_data = get_text_from_file(full_filename)

    text_tags = get_tags_from_text(text_data)

    group_list = parse_to_groups(text_data, text_tags)

    for group in group_list:
        if group['type'] in ('mcq', 'checkbox'):
            group['value'] = SpecialTagParsers.mcq(group['value'])
        elif group['type'] == 'match':
            group['value'] = SpecialTagParsers.match(group['value'])

        if group['value'] == '':
            group['value'] = None

    final_list = []
    for ind in range(0 , len(group_list) , 2) :
        final_list.append((group_list[ind] , group_list[ind + 1]))

    return str(final_list)
    # now, the text data can be parsed


if __name__ == '__main__':
    data = parse_document('C:/Users/Saaransh Jain/Documents/test_temp.txt')
    print(data)
