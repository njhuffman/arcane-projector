from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Block:
    top: int
    right: int
    bottom: int
    left: int

    def rotate(self) -> Block:
        return Block(top=self.left, right=self.top, bottom=self.right, left=self.bottom)


@dataclass(frozen=True)
class Shard:
    blocks: Tuple[Tuple[Block]]
    layers: int

    def __post_init__(self) -> None:
        assert all(len(row) == len(blocks[0]) for row in blocks)

    def _rotate_once(self) -> Shard:
        blocks = list(row[::-1] for row in zip(*blocks))
        for i in range(len(blocks)):
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j].rotate()
        return Shard(blocks=tuple(tuple(row) for row in blocks))

    def rotate(self, n: int) -> Shard:
        new_shard = self
        for i in range(n):
            new_shard = new_shard._rotate_once()
        return new_shard

    def __add__(self, other: Shard) -> Shard:
        assert len(self.blocks) == len(other.blocks)
        new_blocks = []
        for i in range(len(self.blocks)):
            assert len(self.blocks[i]) == len(other.blocks[i])
            row = []
            for j in range(len(self.blocks[i])):
                new_block = Block(
                    top=self.blocks[i][j].top + other.blocks[i][j].top,
                    right=self.blocks[i][j].right + other.blocks[i][j].right,
                    bottom=self.blocks[i][j].bottom + other.blocks[i][j].bottom,
                    left=self.blocks[i][j].left + other.blocks[i][j].left,
                )
                row.append(new_block)
            new_blocks.append(row)
        return Shard(
            layers=self.layers + other.layers,
            blocks=tuple(tuple(row) for row in new_blocks),
        )
