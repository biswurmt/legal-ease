import {
  Box,
  Button,
  Card,
  Container,
  Dialog,
  Heading,
  Icon,
  IconButton,
  Input,
  SimpleGrid,
  Text,
  VStack,
} from "@chakra-ui/react"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useState } from "react"
import { FiTrash2, FiX } from "react-icons/fi"
import { DeleteConfirmationDialog } from "@/components/Common/DeleteConfirmationDialog"
import { toaster } from "@/components/ui/toaster"
import { useCases, useCreateCase, useDeleteCase } from "@/hooks/useCases"

export const Route = createFileRoute("/cases")({
  component: CasesPage,
})

interface Case {
  id: string
  name: string
  last_modified: Date
  scenario_count: number
}

function CasesPage() {
  const navigate = useNavigate()
  const [isNewCaseModalOpen, setIsNewCaseModalOpen] = useState(false)
  const [newCaseTitle, setNewCaseTitle] = useState("")
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [caseToDelete, setCaseToDelete] = useState<Case | null>(null)

  // React Query hooks
  const { data: casesData, isLoading, error } = useCases()
  const createCaseMutation = useCreateCase()
  const deleteCaseMutation = useDeleteCase()

  // Transform data for display
  const cases: Case[] = casesData
    ? casesData.map((c: any) => ({
        id: String(c.id),
        name: c.name,
        last_modified: new Date(c.last_modified),
        scenario_count: c.scenario_count || 0,
      }))
    : []

  const handleNewCase = () => setIsNewCaseModalOpen(true)

  const handleCreateCase = async () => {
    if (!newCaseTitle.trim()) return

    try {
      const newCase = await createCaseMutation.mutateAsync({
        name: newCaseTitle,
        party_a: "",
        party_b: "",
        context: null,
      })

      setIsNewCaseModalOpen(false)
      setNewCaseTitle("")

      // Navigate to the new case
      navigate({ to: "/case", search: { id: String(newCase.id) } })
    } catch (error) {
      console.error("Error creating case:", error)
      toaster.create({
        title: "Error",
        description: "Failed to create case. Please try again.",
        type: "error",
      })
    }
  }

  const handleCancelNewCase = () => {
    setIsNewCaseModalOpen(false)
    setNewCaseTitle("")
  }

  const handleCaseClick = (caseId: string) => {
    navigate({ to: "/case", search: { id: caseId } })
  }

  const handleDeleteClick = (e: React.MouseEvent, caseItem: Case) => {
    e.stopPropagation() // Prevent card click navigation
    setCaseToDelete(caseItem)
    setIsDeleteDialogOpen(true)
  }

  const handleConfirmDelete = async () => {
    if (!caseToDelete) return

    try {
      await deleteCaseMutation.mutateAsync(Number(caseToDelete.id))

      toaster.create({
        title: "Case deleted",
        description: `"${caseToDelete.name}" has been deleted successfully.`,
        type: "success",
      })

      setCaseToDelete(null)
    } catch (error) {
      console.error("Error deleting case:", error)
      toaster.create({
        title: "Error",
        description: "Failed to delete case. Please try again.",
        type: "error",
      })
    }
  }

  const handleCancelDelete = () => {
    setIsDeleteDialogOpen(false)
    setCaseToDelete(null)
  }

  // Show loading state
  if (isLoading) {
    return (
      <Box
        minHeight="100vh"
        bg="#F4ECD8"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <Text fontSize="xl" color="#3A3A3A">
          Loading cases...
        </Text>
      </Box>
    )
  }

  // Show error state
  if (error) {
    return (
      <Box
        minHeight="100vh"
        bg="#F4ECD8"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <Text fontSize="xl" color="red.600">
          Failed to load cases. Please try again.
        </Text>
      </Box>
    )
  }

  return (
    <Box minHeight="100vh" bg="#F4ECD8" py={8}>
      <Container maxW="1200px">
        <Heading fontSize="4xl" fontWeight="semibold" color="#3A3A3A" mb={8}>
          Case Library
        </Heading>

        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6}>
          {/* Existing Cases */}
          {cases.map((caseItem) => (
            <Card.Root
              key={caseItem.id}
              cursor="pointer"
              onClick={() => handleCaseClick(caseItem.id)}
              _hover={{ transform: "scale(1.02)", shadow: "lg" }}
              transition="all 0.2s"
              bg="white"
              position="relative"
            >
              <Card.Body>
                <VStack alignItems="flex-start" gap={4} height="200px">
                  <Heading
                    fontSize="xl"
                    color="#3A3A3A"
                    lineClamp={2}
                    overflow="hidden"
                  >
                    {caseItem.name}
                  </Heading>

                  <VStack alignItems="flex-start" gap={2} flex={1}>
                    <Text fontSize="med" color="#666">
                      Last modified:{" "}
                      {new Date(caseItem.last_modified).toLocaleDateString(
                        "en-US",
                        {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        },
                      )}
                    </Text>
                    <Text fontSize="med" color="#666">
                      {caseItem.scenario_count}{" "}
                      {caseItem.scenario_count === 1
                        ? "simulation"
                        : "simulations"}
                    </Text>
                  </VStack>

                  <IconButton
                    aria-label="Delete case"
                    size="sm"
                    variant="ghost"
                    position="absolute"
                    bottom={2}
                    right={2}
                    onClick={(e) => handleDeleteClick(e, caseItem)}
                    _hover={{ bg: "red.50", color: "red.600" }}
                  >
                    <FiTrash2 />
                  </IconButton>
                </VStack>
              </Card.Body>
            </Card.Root>
          ))}
          {/* New Case Card */}
          <Card.Root
            cursor="pointer"
            onClick={handleNewCase}
            _hover={{ transform: "scale(1.02)", shadow: "lg" }}
            transition="all 0.2s"
            bg="transparent"
            borderWidth="2px"
            borderStyle="dashed"
            borderColor="#D3D3D3"
          >
            <Card.Body>
              <VStack
                height="200px"
                justifyContent="center"
                alignItems="center"
              >
                <Text fontSize="6xl" color="#3A3A3A">
                  +
                </Text>
              </VStack>
            </Card.Body>
          </Card.Root>
        </SimpleGrid>
      </Container>

      {/* New Case Modal */}
      <Dialog.Root
        open={isNewCaseModalOpen}
        onOpenChange={(e) => setIsNewCaseModalOpen(e.open)}
      >
        <Dialog.Backdrop />
        <Dialog.Positioner>
          <Dialog.Content>
            <Dialog.Header>
              <Dialog.Title>Create New Case</Dialog.Title>
              <Dialog.CloseTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCancelNewCase}
                  position="absolute"
                  top={4}
                  right={4}
                >
                  <Icon as={FiX} />
                </Button>
              </Dialog.CloseTrigger>
            </Dialog.Header>
            <Dialog.Body>
              <VStack gap={4} alignItems="flex-start" width="100%">
                <Box width="100%">
                  <Text
                    fontSize="sm"
                    fontWeight="medium"
                    color="#3A3A3A"
                    mb={2}
                  >
                    Case Title
                  </Text>
                  <Input
                    value={newCaseTitle}
                    onChange={(e) => setNewCaseTitle(e.target.value)}
                    placeholder="e.g., Sterling v. Sterling"
                    autoFocus
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleCreateCase()
                      if (e.key === "Escape") handleCancelNewCase()
                    }}
                  />
                </Box>
              </VStack>
            </Dialog.Body>
            <Dialog.Footer>
              <Button
                bg="#3A3A3A"
                color="#F4ECD8"
                _hover={{ bg: "#2A2A2A" }}
                onClick={handleCreateCase}
                disabled={!newCaseTitle.trim()}
              >
                Create Case
              </Button>
            </Dialog.Footer>
          </Dialog.Content>
        </Dialog.Positioner>
      </Dialog.Root>

      {/* Delete Confirmation Dialog */}
      <DeleteConfirmationDialog
        isOpen={isDeleteDialogOpen}
        onClose={handleCancelDelete}
        onConfirm={handleConfirmDelete}
        itemName={caseToDelete?.name || ""}
        itemType="Case"
        warningMessage="This will also delete all associated simulations, messages, and documents. This action cannot be undone."
      />
    </Box>
  )
}
