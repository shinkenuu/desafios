from argparse import ArgumentParser


def break_into_line(text: str, limit: int = 40, justify: bool = False) -> str:
    """
    Break text into lines with delimited size

    :param str text: Text to be broken into lines
    :param int limit: Amount of characters per line to be broken
    :param bool justify: `True` if lines must be justified. `False` otherwise
    :return: text with lines broken
    :rtype: str
    """
    if justify:
        return '\n'.join([
            justify_line(line, limit)
            for line in _fetch_delimited_line(text, limit)])

    return '\n'.join([line for line in _fetch_delimited_line(text, limit)])


def _distribute_whitespaces(whitespaces: list, step: int, amount_to_distribute: int):
    """
    Distribute single whitespaces through intervals and in only one direction.

    :param list whitespaces: the whitespaces to receive the distribution
    :param int step: interval between indexes to receive sparing whitespaces
    :param int amount_to_distribute: amount of sparing whitespaces available for distribution
    :return: amount of whitespaces not distributed
    :rtype: int
    """
    initial_idx = 0 if step > 0 else -1

    for i in range(len(whitespaces[::step])):
        if amount_to_distribute < 1:
            break

        if i == 0:
            whitespaces[initial_idx] += ' '
        else:
            whitespaces[i * step] += ' '

        amount_to_distribute -= 1

    return amount_to_distribute


def justify_line(line: str, limit: int) -> str:
    """
    Justify a line, distributing whitespaces to occupy all available line space.

    :param str line: A already stripped on both sides line with length lesser than `limit`
    :param int limit: maximum amount of characters expected in the final line
    :return: the justified line
    :rtype: str
    """
    line_length = len(line)
    if line_length > limit:
        raise ValueError('line "{}" must be shorter than limit "{}"'.format(line, str(limit)))

    if line_length == limit:
        return line

    amount_of_whitespaces_between_words = line.count(' ')

    if amount_of_whitespaces_between_words < 1:
        return line

    available_characters = limit - len(line)

    available_additional_whitespaces_between_all_words, sparing_whitespaces = \
        divmod(available_characters, amount_of_whitespaces_between_words)

    if available_additional_whitespaces_between_all_words > 0:
        new_whitespaces = [' ' + ' ' * available_additional_whitespaces_between_all_words
                           for _ in range(amount_of_whitespaces_between_words)]

    else:
        new_whitespaces = [' ' for _ in range(amount_of_whitespaces_between_words)]

    if sparing_whitespaces > 0:

        sparing_whitespaces_left = _distribute_whitespaces(new_whitespaces, step=2,
                                                           amount_to_distribute=sparing_whitespaces)

        if sparing_whitespaces_left > 0:
            _distribute_whitespaces(new_whitespaces, step=-2, amount_to_distribute=sparing_whitespaces_left)

    words = line.split(' ')
    zipped_line = ''.join([word + space for word, space in zip(words, new_whitespaces)])
    zipped_line += words[-1]

    return zipped_line


def _fetch_delimited_line(text: str, limit: int) -> str:
    """
    Generate the next delimited line of `text`

    :param text: Text to be delimited into lines
    :param limit: Maximum amount of characters per line
    :return: the delimited line at each yield
    :rtype: generator
    """
    def has_split_last_word():
        if line_end_idx == text_length:
            return False
        return ' ' not in line[-1] + text[line_end_idx]

    line_start_idx = 0
    text_length = len(text)

    while line_start_idx < text_length:
        line_end_idx = line_start_idx + limit

        if line_end_idx > text_length:
            line_end_idx = text_length

        line = text[line_start_idx: line_end_idx]

        if '\n' in line:
            if line.startswith('\n'):
                line_start_idx += 1
                yield ''
                continue

            line_end_idx = line_start_idx + line.find('\n')
            line = text[line_start_idx: line_end_idx]
            line_start_idx = line_end_idx

        elif not has_split_last_word():
            line_start_idx = line_end_idx if line[-1] == ' ' else line_end_idx + 1

        else:
            split_word = line.rsplit(' ', 1)[1]
            split_word_length = len(split_word)

            if split_word_length == limit:
                raise ValueError('"{}" cant be in just one line of {} characters'.format(
                    split_word, str(split_word_length)))

            line = line[0: -split_word_length]
            line_start_idx = line_end_idx - split_word_length

        yield line.strip(' ')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('text', type=str, help='')
    arg_parser.add_argument('limit', type=int, default=40, help='')
    arg_parser.add_argument('justify', nargs='?', type=bool, default=False, help='')

    parsed_args = arg_parser.parse_args()

    received_inputs = ['Text: ' + parsed_args.text,
                       'Limit: ' + str(parsed_args.limit),
                       'Should justify: ' + str(parsed_args.justify),]

    print('\n'.join(received_inputs) + '\n')

    print(break_into_line(text=parsed_args.text, limit=parsed_args.limit, justify=parsed_args.justify))
