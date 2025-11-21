import { Button, Dialog, Icon, Text } from "@chakra-ui/react"
import { FiX } from "react-icons/fi"

interface DeleteConfirmationDialogProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => Promise<void>
  itemName: string
  itemType: string
  warningMessage?: string
}

export function DeleteConfirmationDialog({
  isOpen,
  onClose,
  onConfirm,
  itemName,
  itemType,
  warningMessage,
}: DeleteConfirmationDialogProps) {
  const handleConfirm = async () => {
    await onConfirm()
    onClose()
  }

  return (
    <Dialog.Root open={isOpen} onOpenChange={(e) => !e.open && onClose()}>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content>
          <Dialog.Header>
            <Dialog.Title>Delete {itemType}</Dialog.Title>
            <Dialog.CloseTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                position="absolute"
                top={4}
                right={4}
              >
                <Icon as={FiX} />
              </Button>
            </Dialog.CloseTrigger>
          </Dialog.Header>
          <Dialog.Body>
            <Text>Are you sure you want to delete "{itemName}"?</Text>
            {warningMessage && (
              <Text color="red.600" mt={2}>
                {warningMessage}
              </Text>
            )}
          </Dialog.Body>
          <Dialog.Footer>
            <Button
              bg="red.600"
              color="white"
              _hover={{ bg: "red.700" }}
              onClick={handleConfirm}
            >
              Delete
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Positioner>
    </Dialog.Root>
  )
}
