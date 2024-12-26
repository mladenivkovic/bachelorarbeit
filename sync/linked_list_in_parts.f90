program chair_linkedlist

! This program shows how to create a linked list that is appended to with
! "breaks" in between: Append your "object" to whatever list
! it's supposed to be appended, while the order you "read them in" is
! unknown. (But you know where they should be sorted into.)


! Scenario for this program:
! Assume you have nbuild buildings. In total there are nrooms rooms distributed
! between those 5 buildings (randomly) and every room has nchair chairs.
! The chairs are enumerated by integer numbers. We now want to know what chairs
! can be found in what building.

    implicit none

    ! implementing buildings, rooms and chair indexes
    integer, parameter :: nbuild=5, nchairs=10, nrooms=100
    integer, dimension (1:nrooms, 1:nchairs) :: dummy_chairs_array
    ! contains for every room all chairs and room ID.
    integer, dimension (1:nrooms) :: room_building_ID
    ! building ID of every room.
    real, dimension(1:nrooms) :: randomrealarray
    real :: randomreal
    integer :: dummy_chair_index, empty_room_index


    ! new stuff i want to implement into ramses:
    type chairll
        integer :: chair_index=0
        type(chairll), pointer :: next => null()
    end type chairll
    
    type (chairll), allocatable, dimension(:,:), target :: buildingchairs
    !two dimensional array for linked lists of chairs that belong to a building
    !first index: room id
    !second index: first and last chair of list


    ! looping variables, counters:
    integer :: i, j, k, building_id, iroom, index, ichair, firstchair
    logical :: relevant
    type (chairll), pointer :: lastchair_ll, thischair_ll

    !comparison
    integer, dimension(1:nbuild) :: total_chairs_control, total_chairs_ll
    integer, dimension(:,:),allocatable :: ci_ll, ci_c !chair index array
    integer :: maxchairs_c



!---------------------------------------
!--- CREATING IMAGINARY ROOMS AND CHAIRS ARRAYS
!--- ASSIGNING CONTROL ARRAYS
!---------------------------------------

    total_chairs_control=0 !initiate array to 0

    !Fill up array with rooms containing chairs with chair indices,
    !assign every room a building_id randomly.

    ! create a random number for every room
    call random_seed
    call random_number(randomrealarray)

    dummy_chair_index=1
    ! creating dummy array for rooms and chairs
    do j=1, nrooms
    
        !give every room a random building id
        building_id=int(randomrealarray(j)*nbuild)+1
        room_building_ID(j)=building_id

        do k=1, nchairs
            ! give every chair an index
            dummy_chairs_array(j,k)=dummy_chair_index
            dummy_chair_index=dummy_chair_index+1
        end do
        
        ! calculate total chairs per room
        total_chairs_control(building_id)=total_chairs_control(building_id)+nchairs ! ok since every room has same nr of chairs...
    end do


    !getting highest number of chairs per room id for array allocation
    maxchairs_c=total_chairs_control(1)
    do i=2, nbuild
        if (total_chairs_control(i)>maxchairs_c) maxchairs_c=total_chairs_control(i)
    end do

    allocate(ci_c(1:nbuild,1:maxchairs_c))
    ci_c=-1
    
    
    !distribute chair indexes
    do i=1, nbuild
        index=1
        do j=1, nrooms
            if (room_building_ID(j)==i) then
                do k=1, nchairs
                    ci_c(i,index)=dummy_chairs_array(j,k)
                    index=index+1
                end do
            end if
        end do
    end do






!---------------------------------------
!-- CREATING LINKED LISTS
!---------------------------------------



    allocate(buildingchairs(1:nbuild, 1:2))
    
    write(*,*) "Entering linked lists"
    do iroom=1, nrooms
        building_id = room_building_ID(iroom) 
        !check if already chairs are assigned
        if (associated(buildingchairs(building_id,1)%next)) then
            ! if yes: start appending the list after the past chair
            thischair_ll=>buildingchairs(building_id,2)%next
        else
            !assign first chair of this room as first chair of linked list 
            !for this room
            thischair_ll=>buildingchairs(building_id,1)
        end if

        do ichair=1,nchairs
            !get chair index
            index=dummy_chairs_array(iroom,ichair)
            thischair_ll%chair_index=index
            !allocate next
            allocate(thischair_ll%next)
            !switch to next
            thischair_ll=>thischair_ll%next
        end do

        !rewrite the last chair of buildingchairs
        buildingchairs(building_id,2)%next=>thischair_ll

    end do

    write(*,*) "Done linked lists"






!---------------------------------------
!-- GATHERING DATA FROM LINKED LISTS
!---------------------------------------
    

    do i=1, nbuild
    write(*,*) "Building",i,"first chair index", buildingchairs(i,1)%chair_index
    !write(*,*) "last index", buildingchairs(i,2)%chair_index ! should be =0 ...
        ! gathering total chairs per building
        ichair=0
        thischair_ll=>buildingchairs(i,1)
        do while (associated(thischair_ll%next))
            ichair=ichair+1
            thischair_ll=>thischair_ll%next
        end do
        total_chairs_ll(i) = ichair
    end do







!---------------------------------------
!-- WRITE OUTPUT
!---------------------------------------
   

    call output_totalchair
    call output_index
    

contains



subroutine output_totalchair()

    ! write the number of total chairs per building
    implicit none

    write(*,*)
    write(*, '(A17,x,x,x,x,x,A17)') "control array", "linked list array"
    write(*, '(A8,x,A8,x,x,x,x,x,A8,x,A8)') "building_id", "tot_chairs", "building_id", "tot_chairs"
    do i=1,nbuild
        write(*, '(I8,x,I8,x,x,x,x,x,I8,x,I8)') i, total_chairs_control(i), i, total_chairs_ll(i)
    end do
    write(*, '(A8,x,I8,x,x,x,x,x,A8,x,I8)') "Total:", sum(total_chairs_control(:)),"",sum(total_chairs_ll(:))

end subroutine output_totalchair




subroutine output_index
    !write every chair in building by index 
    implicit none
    do j=1, nbuild
    write(*,*)
    write(*,*) "--------------------"
    write(*,*) "building", j
    write(*,*) "--------------------"
    write(*,'(2A8)') "control", "list"
    thischair_ll=>buildingchairs(j,1)
        do i=1, maxchairs_c
            index=-1
            if(associated(thischair_ll%next)) then
                index=thischair_ll%chair_index
                thischair_ll=>thischair_ll%next
            end if

            write(*, '(2I8)') ci_c(j, i), index 
        end do
    end do

end subroutine output_index


subroutine output_cp
    ! print all cells with chairs and room IDs
    implicit none

    write(*,*)
     do i=1, nrooms
        write(*, '(I4,xxx,10I4)') (dummy_chairs_array(i,j), j=1, nchairs+1) 
    end do
end subroutine output_cp







end program chair_linkedlist
