/**
 * Tests for tree utility functions.
 * Ensures tree manipulation logic remains correct during refactoring.
 */
import { describe, it, expect } from 'vitest'
import {
  getPartyFromRole,
  messageToDialogueNode,
  buildDialogueTreeFromMessages,
  findNodeInTree,
} from './treeUtils'
import type { TreeMessagesResponse, DialogueNode } from '@/types/scenario'

describe('Tree Utilities', () => {
  describe('getPartyFromRole', () => {
    it('should map "A" to Party A', () => {
      expect(getPartyFromRole('A')).toBe('A')
      expect(getPartyFromRole('a')).toBe('A')
      expect(getPartyFromRole(' A ')).toBe('A')
    })

    it('should map "B" to Party B', () => {
      expect(getPartyFromRole('B')).toBe('B')
      expect(getPartyFromRole('b')).toBe('B')
      expect(getPartyFromRole(' B ')).toBe('B')
    })

    it('should handle legacy "user" format', () => {
      expect(getPartyFromRole('user')).toBe('A')
      expect(getPartyFromRole('USER')).toBe('A')
      expect(getPartyFromRole('party a')).toBe('A')
    })

    it('should handle legacy "assistant" format', () => {
      expect(getPartyFromRole('assistant')).toBe('B')
      expect(getPartyFromRole('ASSISTANT')).toBe('B')
      expect(getPartyFromRole('party b')).toBe('B')
    })

    it('should default to Party A for unknown roles', () => {
      expect(getPartyFromRole('unknown')).toBe('A')
      expect(getPartyFromRole('system')).toBe('A')
      expect(getPartyFromRole('')).toBe('A')
    })
  })

  describe('messageToDialogueNode', () => {
    it('should convert simple message to DialogueNode', () => {
      const message: TreeMessagesResponse = {
        id: 1,
        content: 'Hello',
        role: 'A',
        selected: true,
        simulation_id: 1,
        parent_id: null,
        children: []
      }

      const node = messageToDialogueNode(message, false)

      expect(node.id).toBe('1')
      expect(node.statement).toBe('Hello')
      expect(node.party).toBe('A')
      expect(node.role).toBe('A')
      expect(node.selected).toBe(true)
      expect(node.children).toEqual([])
    })

    it('should convert message with children when includeChildren is true', () => {
      const message: TreeMessagesResponse = {
        id: 1,
        content: 'Parent',
        role: 'A',
        selected: true,
        simulation_id: 1,
        parent_id: null,
        children: [
          {
            id: 2,
            content: 'Child 1',
            role: 'B',
            selected: false,
            simulation_id: 1,
            parent_id: 1,
            children: []
          },
          {
            id: 3,
            content: 'Child 2',
            role: 'B',
            selected: false,
            simulation_id: 1,
            parent_id: 1,
            children: []
          }
        ]
      }

      const node = messageToDialogueNode(message, true)

      expect(node.children.length).toBe(2)
      expect(node.children[0].id).toBe('2')
      expect(node.children[0].statement).toBe('Child 1')
      expect(node.children[1].id).toBe('3')
      expect(node.children[1].statement).toBe('Child 2')
    })

    it('should not include children when includeChildren is false', () => {
      const message: TreeMessagesResponse = {
        id: 1,
        content: 'Parent',
        role: 'A',
        selected: true,
        simulation_id: 1,
        parent_id: null,
        children: [
          {
            id: 2,
            content: 'Child',
            role: 'B',
            selected: false,
            simulation_id: 1,
            parent_id: 1,
            children: []
          }
        ]
      }

      const node = messageToDialogueNode(message, false)

      expect(node.children).toEqual([])
    })

    it('should handle nested children recursively', () => {
      const message: TreeMessagesResponse = {
        id: 1,
        content: 'Grandparent',
        role: 'A',
        selected: true,
        simulation_id: 1,
        parent_id: null,
        children: [
          {
            id: 2,
            content: 'Parent',
            role: 'B',
            selected: true,
            simulation_id: 1,
            parent_id: 1,
            children: [
              {
                id: 3,
                content: 'Child',
                role: 'A',
                selected: false,
                simulation_id: 1,
                parent_id: 2,
                children: []
              }
            ]
          }
        ]
      }

      const node = messageToDialogueNode(message, true)

      expect(node.children[0].children.length).toBe(1)
      expect(node.children[0].children[0].id).toBe('3')
      expect(node.children[0].children[0].statement).toBe('Child')
    })
  })

  describe('buildDialogueTreeFromMessages', () => {
    it('should return null for empty messages array', () => {
      const tree = buildDialogueTreeFromMessages([])
      expect(tree).toBeNull()
    })

    it('should build tree from single root message', () => {
      const messages: TreeMessagesResponse[] = [
        {
          id: 1,
          content: 'Root',
          role: 'A',
          selected: true,
          simulation_id: 1,
          parent_id: null,
          children: []
        }
      ]

      const tree = buildDialogueTreeFromMessages(messages)

      expect(tree).not.toBeNull()
      expect(tree?.id).toBe('1')
      expect(tree?.statement).toBe('Root')
    })

    it('should build tree with nested structure', () => {
      const messages: TreeMessagesResponse[] = [
        {
          id: 1,
          content: 'Root',
          role: 'A',
          selected: true,
          simulation_id: 1,
          parent_id: null,
          children: [
            {
              id: 2,
              content: 'Child 1',
              role: 'B',
              selected: true,
              simulation_id: 1,
              parent_id: 1,
              children: [
                {
                  id: 3,
                  content: 'Grandchild',
                  role: 'A',
                  selected: false,
                  simulation_id: 1,
                  parent_id: 2,
                  children: []
                }
              ]
            },
            {
              id: 4,
              content: 'Child 2',
              role: 'B',
              selected: false,
              simulation_id: 1,
              parent_id: 1,
              children: []
            }
          ]
        }
      ]

      const tree = buildDialogueTreeFromMessages(messages)

      expect(tree?.children.length).toBe(2)
      expect(tree?.children[0].children.length).toBe(1)
      expect(tree?.children[0].children[0].id).toBe('3')
    })
  })

  describe('findNodeInTree', () => {
    const sampleTree: DialogueNode = {
      id: '1',
      statement: 'Root',
      party: 'A',
      role: 'A',
      selected: true,
      children: [
        {
          id: '2',
          statement: 'Child 1',
          party: 'B',
          role: 'B',
          selected: true,
          children: [
            {
              id: '3',
              statement: 'Grandchild',
              party: 'A',
              role: 'A',
              selected: false,
              children: []
            }
          ]
        },
        {
          id: '4',
          statement: 'Child 2',
          party: 'B',
          role: 'B',
          selected: false,
          children: []
        }
      ]
    }

    it('should return null for null tree', () => {
      const result = findNodeInTree(null, '1')
      expect(result).toBeNull()
    })

    it('should find root node', () => {
      const result = findNodeInTree(sampleTree, '1')
      expect(result).not.toBeNull()
      expect(result?.id).toBe('1')
      expect(result?.statement).toBe('Root')
    })

    it('should find direct child', () => {
      const result = findNodeInTree(sampleTree, '2')
      expect(result).not.toBeNull()
      expect(result?.id).toBe('2')
      expect(result?.statement).toBe('Child 1')
    })

    it('should find deeply nested node', () => {
      const result = findNodeInTree(sampleTree, '3')
      expect(result).not.toBeNull()
      expect(result?.id).toBe('3')
      expect(result?.statement).toBe('Grandchild')
    })

    it('should return null for non-existent node', () => {
      const result = findNodeInTree(sampleTree, '999')
      expect(result).toBeNull()
    })

    it('should find sibling nodes', () => {
      const child1 = findNodeInTree(sampleTree, '2')
      const child2 = findNodeInTree(sampleTree, '4')

      expect(child1).not.toBeNull()
      expect(child2).not.toBeNull()
      expect(child1?.id).toBe('2')
      expect(child2?.id).toBe('4')
    })
  })
})
