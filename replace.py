#!/usr/bin/env python2.7

import argparse
import re
import sys

def writeTodo(lines, todo_file):
    f = open(todo_file, 'w')
    for line in lines:
        f.write("%s" % line)
    f.close()

def composeItem(priority, projects, contexts, message):
    item = priority.strip() + ' ' + message.strip() + ' '
    for project in projects:
        item = item + project.strip() + ' '
    for context in contexts:
        item = item + context.strip() + ' '

    return item.strip() + "\n"


def main(argv):
    description = """
TODO.TXT Extended Replace
"""
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-c', '--context', help="Replace context")
    parser.add_argument('-p', '--project', help="Replace project")
    parser.add_argument('-m', '--message', help="Replace message")
    parser.add_argument('todo_file')
    parser.add_argument('item_number', type=int)
    parser.add_argument('text', nargs='?')

    args = parser.parse_args(argv)

    real_item_number = args.item_number - 1

    f = open(args.todo_file)
    lines = f.readlines()
    f.close()

    if real_item_number > len(lines):
        sys.exit('Item does not exist')

    item = lines[real_item_number]

    priority = ''
    priority_match = re.match('(^\([a-zA-Z]\))', item)
    if priority_match:
        priority = priority_match.group(0)

    projects = ()
    project_match = re.search('(\+\w+)', item)
    if project_match:
        projects = project_match.groups()

    contexts = ()
    context_match = re.search('(@\w+)', item)
    if context_match:
        contexts = context_match.groups()

    message = item
    message = message.replace(priority, '')
    for project in projects:
        message = message.replace(project, '')
    for context in contexts:
        message = message.replace(context, '')
    message = message.strip()

    if not (args.context or args.project or args.message):
        lines[real_item_number] = priority + ' ' + args.text + "\n"
        writeTodo(lines, args.todo_file)
        return

    if args.context:
        contexts = (args.context,)

    if args.project:
        projects = (args.project,)

    if args.message:
        message = args.message

    lines[real_item_number] = composeItem(
        priority,
        projects,
        contexts,
        message
    )
    writeTodo(lines, args.todo_file)
    return

if __name__ == "__main__":
    main(sys.argv[1:])