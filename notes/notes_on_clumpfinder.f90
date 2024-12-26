subroutine clump_finder

	subroutine make_tree_fine:
          ! This subroutine checks if particles have moved from their parent grid
	  ! to one of the 3**ndim neighboring sister grids. The particle is then 
	  ! disconnected from the parent grid linked list, and connected to the
	  ! corresponding sister grid linked list. If the sister grid does
	  ! not exist, the particle is left to its original parent grid.
	  ! Particles must not move to a distance greater than direct neighbors
	  ! boundaries. Otherwise an error message is issued and the code stops.

	subroutine kill_tree_fine:
  	  ! This routine sorts particle between ilevel grids and their 
  	  ! ilevel+1 children grids. Particles are disconnected from their parent 
  	  ! grid linked list and connected to their corresponding child grid linked 
  	  ! list. If the  child grid does not exist, the particle is left to its 
  	  ! original parent grid. 
  	  
  	subroutine virtual_tree_fine:
  	  ! This subroutine move particles across processors boundaries.
  	  
  	subroutine merge_tree_fine 
  	  ! This routine disconnects all particles contained in children grids
  	  ! and connects them to their parent grid linked list.
