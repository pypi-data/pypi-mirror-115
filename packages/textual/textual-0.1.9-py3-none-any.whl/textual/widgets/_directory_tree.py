from __future__ import annotations

from dataclasses import dataclass
from os import scandir
import os.path

from rich.console import RenderableType
import rich.repr
from rich.text import Text
from rich.tree import Tree

from .. import events
from ..message import Message
from .._types import MessageTarget
from . import TreeControl, TreeClick, TreeNode, NodeID


@dataclass
class DirEntry:
    path: str
    is_dir: bool


@rich.repr.auto
class FileClick(Message, bubble=True):
    def __init__(self, sender: MessageTarget, path: str) -> None:
        self.path = path
        super().__init__(sender)


class DirectoryTree(TreeControl[DirEntry]):
    def __init__(self, path: str, name: str = None) -> None:
        self.path = path.rstrip("/")
        label = os.path.basename(self.path)
        data = DirEntry(path, True)
        super().__init__(label, name=name, data=data)
        self.root.tree.guide_style = "black"

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():
            node.tree.guide_style = (
                "bold not dim red" if node.id == hover_node else "black"
            )
        self.refresh(layout=True)

    def render_node(self, node: TreeNode[DirEntry]) -> RenderableType:
        meta = {"@click": f"click_label({node.id})", "tree_node": node.id}
        label = Text(node.label) if isinstance(node.label, str) else node.label
        if node.id == self.hover_node:
            label.stylize("underline")
        if node.data.is_dir:
            label.stylize("bold magenta")
            icon = "📂" if node.expanded else "📁"
        else:
            label.stylize("bright_green")
            icon = "📄"
            label.highlight_regex(r"\..*$", "green")

        if label.plain.startswith("."):
            label.stylize("dim")

        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)
        return icon_label

    async def on_mount(self, event: events.Mount) -> None:
        await self.load_directory(self.root)

    async def load_directory(self, node: TreeNode[DirEntry]):
        path = node.data.path
        directory = sorted(
            list(scandir(path)), key=lambda entry: (not entry.is_dir(), entry.name)
        )
        for entry in directory:
            await node.add(entry.name, DirEntry(entry.path, entry.is_dir()))
        node.loaded = True
        await node.expand()
        # self.refresh(layout=True)

    async def message_tree_click(self, message: TreeClick[DirEntry]) -> None:
        dir_entry = message.node.data
        if not dir_entry.is_dir:
            await self.emit(FileClick(self, dir_entry.path))
        else:
            if not message.node.loaded:
                await self.load_directory(message.node)
                await message.node.expand()
            else:
                await message.node.toggle()


if __name__ == "__main__":
    from textual import events
    from textual.app import App

    class TreeApp(App):
        async def on_mount(self, event: events.Mount) -> None:
            await self.view.dock(DirectoryTree("/Users/willmcgugan/projects"))

    TreeApp.run(log="textual.log")
